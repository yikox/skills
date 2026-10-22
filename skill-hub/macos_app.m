#import <Cocoa/Cocoa.h>
#import <WebKit/WebKit.h>
#include <signal.h>
#include <unistd.h>

@interface SkillHubAppDelegate : NSObject <NSApplicationDelegate, NSWindowDelegate, WKNavigationDelegate>
@property (nonatomic, strong) NSWindow *window;
@property (nonatomic, strong) WKWebView *webView;
@property (nonatomic, strong) NSStatusItem *statusItem;
@property (nonatomic, strong) NSMenuItem *statusLabelItem;
@property (nonatomic, strong) NSTimer *healthTimer;
@property (nonatomic, copy) NSString *hubDir;
@property (nonatomic, copy) NSString *serverUrl;
@property (nonatomic, assign) BOOL hasLoadedInitialPage;
@end

@implementation SkillHubAppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)notification {
    [NSApp setActivationPolicy:NSApplicationActivationPolicyRegular];

    NSDictionary *env = [[NSProcessInfo processInfo] environment];
    self.hubDir = env[@"SKILL_HUB_DIR"] ?: [NSHomeDirectory() stringByAppendingPathComponent:@"Work/skills/skill-hub"];
    NSString *port = env[@"SKILL_HUB_PORT"] ?: @"8788";
    self.serverUrl = [NSString stringWithFormat:@"http://127.0.0.1:%@", port];

    [self setupMainMenu];
    [self setupStatusItem];
    [self setupMainWindow];

    // 启动后台 Python 服务并加载界面
    [self ensureServerStartedAndLoad];

    // 定时检测后端进程是否存在（若用户在页面内点击了「关闭服务」，App 窗口自动同步退出）
    self.healthTimer = [NSTimer scheduledTimerWithTimeInterval:0.8
                                                        target:self
                                                      selector:@selector(checkBackendAlive)
                                                      userInfo:nil
                                                       repeats:YES];

    [NSApp activateIgnoringOtherApps:YES];
}

- (void)setupMainMenu {
    NSMenu *menubar = [[NSMenu alloc] init];
    [NSApp setMainMenu:menubar];

    // 1. 应用菜单
    NSMenuItem *appMenuItem = [[NSMenuItem alloc] init];
    [menubar addItem:appMenuItem];
    NSMenu *appMenu = [[NSMenu alloc] initWithTitle:@"Skill Hub"];
    [appMenu addItemWithTitle:@"重新加载面板" action:@selector(reloadWebView:) keyEquivalent:@"r"];
    [appMenu addItemWithTitle:@"在默认浏览器中打开" action:@selector(openInBrowser:) keyEquivalent:@"b"];
    [appMenu addItem:[NSMenuItem separatorItem]];
    [appMenu addItemWithTitle:@"退出 Skill Hub（同时停止服务）" action:@selector(terminate:) keyEquivalent:@"q"];
    [appMenuItem setSubmenu:appMenu];

    // 2. 编辑菜单（确保 WKWebView 内支持 Cmd+C / Cmd+V / Cmd+A / Cmd+Z）
    NSMenuItem *editMenuItem = [[NSMenuItem alloc] init];
    [menubar addItem:editMenuItem];
    NSMenu *editMenu = [[NSMenu alloc] initWithTitle:@"编辑"];
    [editMenu addItemWithTitle:@"撤销" action:@selector(undo:) keyEquivalent:@"z"];
    [editMenu addItemWithTitle:@"重做" action:@selector(redo:) keyEquivalent:@"Z"];
    [editMenu addItem:[NSMenuItem separatorItem]];
    [editMenu addItemWithTitle:@"剪切" action:@selector(cut:) keyEquivalent:@"x"];
    [editMenu addItemWithTitle:@"复制" action:@selector(copy:) keyEquivalent:@"c"];
    [editMenu addItemWithTitle:@"粘贴" action:@selector(paste:) keyEquivalent:@"v"];
    [editMenu addItemWithTitle:@"全选" action:@selector(selectAll:) keyEquivalent:@"a"];
    [editMenuItem setSubmenu:editMenu];
}

- (void)setupStatusItem {
    self.statusItem = [[NSStatusBar systemStatusBar] statusItemWithLength:NSVariableStatusItemLength];
    if (self.statusItem.button) {
        self.statusItem.button.title = @"⚡ Skill Hub";
    }
    NSMenu *menu = [[NSMenu alloc] init];
    self.statusLabelItem = [[NSMenuItem alloc] initWithTitle:@"🟢 服务运行中 (127.0.0.1:8788)" action:nil keyEquivalent:@""];
    [self.statusLabelItem setEnabled:NO];
    [menu addItem:self.statusLabelItem];
    [menu addItem:[NSMenuItem separatorItem]];
    [menu addItemWithTitle:@"显示主窗口" action:@selector(showMainWindow:) keyEquivalent:@""];
    [menu addItemWithTitle:@"在浏览器中打开" action:@selector(openInBrowser:) keyEquivalent:@""];
    [menu addItem:[NSMenuItem separatorItem]];
    [menu addItemWithTitle:@"🛑 关闭服务并退出" action:@selector(terminate:) keyEquivalent:@"q"];
    self.statusItem.menu = menu;
}

- (void)setupMainWindow {
    NSRect frame = NSMakeRect(0, 0, 1400, 860);
    NSUInteger style = NSWindowStyleMaskTitled |
                       NSWindowStyleMaskClosable |
                       NSWindowStyleMaskMiniaturizable |
                       NSWindowStyleMaskResizable;

    self.window = [[NSWindow alloc] initWithContentRect:frame
                                              styleMask:style
                                                backing:NSBackingStoreBuffered
                                                  defer:NO];
    [self.window setTitle:@"⚡ Skill Hub — 本地 Skill 管家 & 快捷启动台  [🟢 运行中 · 关闭此窗口即停止后台服务]"];
    [self.window setMinSize:NSMakeSize(960, 600)];
    [self.window center];
    [self.window setDelegate:self];

    WKWebViewConfiguration *config = [[WKWebViewConfiguration alloc] init];
    self.webView = [[WKWebView alloc] initWithFrame:[[self.window contentView] bounds] configuration:config];
    [self.webView setAutoresizingMask:(NSViewWidthSizable | NSViewHeightSizable)];
    [self.webView setNavigationDelegate:self];

    [[self.window contentView] addSubview:self.webView];
    [self.window makeKeyAndOrderFront:nil];
}

- (void)runCtlCommand:(NSString *)subcommand {
    NSString *ctlPath = [self.hubDir stringByAppendingPathComponent:@"ctl.sh"];
    NSTask *task = [[NSTask alloc] init];
    [task setLaunchPath:@"/bin/bash"];
    [task setArguments:@[ctlPath, subcommand]];
    [task setStandardOutput:[NSPipe pipe]];
    [task setStandardError:[NSPipe pipe]];
    @try {
        [task launch];
        [task waitUntilExit];
    } @catch (NSException *exception) {
    }
}

- (void)ensureServerStartedAndLoad {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        [self runCtlCommand:@"start-headless"];
        NSString *portFile = [self.hubDir stringByAppendingPathComponent:@"vault/server.port"];
        NSString *actualPort = [[NSString stringWithContentsOfFile:portFile encoding:NSUTF8StringEncoding error:nil]
                                stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
        dispatch_async(dispatch_get_main_queue(), ^{
            if (actualPort.length > 0) {
                self.serverUrl = [NSString stringWithFormat:@"http://127.0.0.1:%@", actualPort];
                [self.statusLabelItem setTitle:[NSString stringWithFormat:@"🟢 服务运行中 (127.0.0.1:%@)", actualPort]];
            }
            self.hasLoadedInitialPage = YES;
            NSURL *url = [NSURL URLWithString:self.serverUrl];
            [self.webView loadRequest:[NSURLRequest requestWithURL:url]];
        });
    });
}

- (void)checkBackendAlive {
    if (!self.hasLoadedInitialPage) {
        return;
    }
    NSString *pidFile = [self.hubDir stringByAppendingPathComponent:@"vault/server.pid"];
    if (![[NSFileManager defaultManager] fileExistsAtPath:pidFile]) {
        // 后端已被网页端「关闭服务」停止，立刻关闭窗口并退出 App
        [self.healthTimer invalidate];
        self.healthTimer = nil;
        [NSApp terminate:nil];
        return;
    }
    NSString *pidStr = [[NSString stringWithContentsOfFile:pidFile encoding:NSUTF8StringEncoding error:nil]
                        stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
    if (pidStr.length > 0) {
        pid_t pid = (pid_t)[pidStr intValue];
        if (pid > 0 && kill(pid, 0) != 0) {
            [self.healthTimer invalidate];
            self.healthTimer = nil;
            [NSApp terminate:nil];
        }
    }
}

- (void)reloadWebView:(id)sender {
    [self.webView reload];
}

- (void)openInBrowser:(id)sender {
    [[NSWorkspace sharedWorkspace] openURL:[NSURL URLWithString:self.serverUrl]];
}

- (void)showMainWindow:(id)sender {
    [self.window makeKeyAndOrderFront:nil];
    [NSApp activateIgnoringOtherApps:YES];
}

- (BOOL)applicationShouldHandleReopen:(NSApplication *)theApplication hasVisibleWindows:(BOOL)flag {
    if (!flag) {
        [self.window makeKeyAndOrderFront:nil];
    }
    [NSApp activateIgnoringOtherApps:YES];
    return YES;
}

// 关闭窗口即退出 App（从而触发 applicationWillTerminate 自动停止后端服务）
- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *)sender {
    return YES;
}

- (void)applicationWillTerminate:(NSNotification *)notification {
    [self.healthTimer invalidate];
    self.healthTimer = nil;
    [self runCtlCommand:@"stop"];
}

@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSApplication *app = [NSApplication sharedApplication];
        SkillHubAppDelegate *delegate = [[SkillHubAppDelegate alloc] init];
        [app setDelegate:delegate];
        [app run];
    }
    return 0;
}
