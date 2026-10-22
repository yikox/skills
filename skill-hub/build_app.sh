#!/bin/bash
set -euo pipefail

# build_app.sh - 编译原生 Skill Hub.app、生成 macOS 高清图标 (AppIcon.icns) 并同步到 /Applications

HUB_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_BUNDLE="${HUB_DIR}/Skill Hub.app"
CONTENTS_DIR="${APP_BUNDLE}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"
TMP_DIR="$(mktemp -d)"

trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$MACOS_DIR" "$RESOURCES_DIR"

# 1. 使用 Cocoa CoreGraphics 生成 1024x1024 矢量图标 PNG
cat >"${TMP_DIR}/gen_icon.m" <<'EOF'
#import <Cocoa/Cocoa.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        if (argc < 2) return 1;
        NSString *outPath = [NSString stringWithUTF8String:argv[1]];
        int size = 1024;

        NSBitmapImageRep *rep = [[NSBitmapImageRep alloc]
            initWithBitmapDataPlanes:NULL
                          pixelsWide:size
                          pixelsHigh:size
                       bitsPerSample:8
                     samplesPerPixel:4
                            hasAlpha:YES
                            isPlanar:NO
                      colorSpaceName:NSCalibratedRGBColorSpace
                         bytesPerRow:0
                        bitsPerPixel:0];

        [NSGraphicsContext saveGraphicsState];
        NSGraphicsContext *ctx = [NSGraphicsContext graphicsContextWithBitmapImageRep:rep];
        [NSGraphicsContext setCurrentContext:ctx];

        // 1) macOS 圆角矩形基底 (留出标准 96px 边距)
        NSRect cardRect = NSMakeRect(88, 88, 848, 848);
        NSBezierPath *cardPath = [NSBezierPath bezierPathWithRoundedRect:cardRect xRadius:190 yRadius:190];

        // 深邃蓝紫科技渐变背景
        NSColor *cTop = [NSColor colorWithCalibratedRed:0.10 green:0.16 blue:0.36 alpha:1.0];
        NSColor *cMid = [NSColor colorWithCalibratedRed:0.06 green:0.09 blue:0.20 alpha:1.0];
        NSColor *cBot = [NSColor colorWithCalibratedRed:0.03 green:0.05 blue:0.11 alpha:1.0];
        NSGradient *bgGrad = [[NSGradient alloc] initWithColors:@[cBot, cMid, cTop]];
        [bgGrad drawInBezierPath:cardPath angle:90.0];

        // 顶部柔和霓虹高光晕
        [cardPath addClip];
        NSBezierPath *glowPath = [NSBezierPath bezierPathWithOvalInRect:NSMakeRect(160, 520, 704, 520)];
        NSGradient *glowGrad = [[NSGradient alloc] initWithStartingColor:[NSColor colorWithCalibratedRed:0.22 green:0.58 blue:0.98 alpha:0.28]
                                                             endingColor:[NSColor colorWithCalibratedRed:0.22 green:0.58 blue:0.98 alpha:0.0]];
        [glowGrad drawInBezierPath:glowPath relativeCenterPosition:NSMakePoint(0, 0)];

        // 2) 中心 Hub 六边形连接环
        NSBezierPath *hexRing = [NSBezierPath bezierPathWithRoundedRect:NSMakeRect(220, 250, 584, 540) xRadius:130 yRadius:130];
        [hexRing setLineWidth:10.0];
        [[NSColor colorWithCalibratedRed:0.25 green:0.62 blue:1.0 alpha:0.25] setStroke];
        [hexRing stroke];

        // 四个角的 Skill 节点圆点
        NSPoint nodes[4] = {
            NSMakePoint(250, 690),
            NSMakePoint(774, 690),
            NSMakePoint(250, 350),
            NSMakePoint(774, 350)
        };
        for (int i = 0; i < 4; i++) {
            NSRect nr = NSMakeRect(nodes[i].x - 22, nodes[i].y - 22, 44, 44);
            NSBezierPath *np = [NSBezierPath bezierPathWithOvalInRect:nr];
            [[NSColor colorWithCalibratedRed:0.22 green:0.82 blue:0.96 alpha:0.85] setFill];
            [np fill];
        }

        // 3) 中心金色/青色闪电符号 (⚡)
        NSBezierPath *bolt = [NSBezierPath bezierPath];
        [bolt moveToPoint:NSMakePoint(565, 790)];
        [bolt lineToPoint:NSMakePoint(335, 495)];
        [bolt lineToPoint:NSMakePoint(490, 495)];
        [bolt lineToPoint:NSMakePoint(445, 255)];
        [bolt lineToPoint:NSMakePoint(695, 550)];
        [bolt lineToPoint:NSMakePoint(535, 550)];
        [bolt closePath];

        NSGradient *boltGrad = [[NSGradient alloc] initWithColors:@[
            [NSColor colorWithCalibratedRed:1.00 green:0.65 blue:0.10 alpha:1.0],
            [NSColor colorWithCalibratedRed:1.00 green:0.88 blue:0.28 alpha:1.0]
        ]];
        [boltGrad drawInBezierPath:bolt angle:90.0];

        [bolt setLineWidth:8.0];
        [[NSColor colorWithCalibratedWhite:1.0 alpha:0.65] setStroke];
        [bolt stroke];

        // 4) 底部 "HUB" 胶囊标签
        NSRect pillRect = NSMakeRect(342, 138, 340, 76);
        NSBezierPath *pill = [NSBezierPath bezierPathWithRoundedRect:pillRect xRadius:38 yRadius:38];
        [[NSColor colorWithCalibratedRed:0.12 green:0.53 blue:0.96 alpha:0.92] setFill];
        [pill fill];

        NSDictionary *attrs = @{
            NSFontAttributeName: [NSFont systemFontOfSize:44 weight:NSFontWeightHeavy],
            NSForegroundColorAttributeName: [NSColor whiteColor]
        };
        NSString *label = @"SKILL HUB";
        NSSize textSize = [label sizeWithAttributes:attrs];
        NSPoint textPt = NSMakePoint(NSMidX(pillRect) - textSize.width / 2.0,
                                     NSMidY(pillRect) - textSize.height / 2.0 + 2);
        [label drawAtPoint:textPt withAttributes:attrs];

        // 5) 外框亮边
        [cardPath setLineWidth:12.0];
        [[NSColor colorWithCalibratedRed:0.35 green:0.65 blue:1.0 alpha:0.42] setStroke];
        [cardPath stroke];

        [NSGraphicsContext restoreGraphicsState];

        NSData *pngData = [rep representationUsingType:NSBitmapImageFileTypePNG properties:@{}];
        [pngData writeToFile:outPath atomically:YES];
    }
    return 0;
}
EOF

/usr/bin/clang -O2 -fobjc-arc -framework Cocoa "${TMP_DIR}/gen_icon.m" -o "${TMP_DIR}/gen_icon"
MASTER_PNG="${TMP_DIR}/icon_1024.png"
"${TMP_DIR}/gen_icon" "$MASTER_PNG"

# 2. 构建标准 .iconset 并打包为 AppIcon.icns
ICONSET_DIR="${TMP_DIR}/AppIcon.iconset"
mkdir -p "$ICONSET_DIR"

for sz in 16 32 128 256 512; do
  /usr/bin/sips -z "$sz" "$sz" "$MASTER_PNG" --out "${ICONSET_DIR}/icon_${sz}x${sz}.png" >/dev/null
  sz2=$((sz * 2))
  /usr/bin/sips -z "$sz2" "$sz2" "$MASTER_PNG" --out "${ICONSET_DIR}/icon_${sz}x${sz}@2x.png" >/dev/null
done

/usr/bin/iconutil -c icns "$ICONSET_DIR" -o "${RESOURCES_DIR}/AppIcon.icns"

# 3. 直接将 macos_app.m 编译为包内原生可执行文件 Contents/MacOS/SkillHub
/usr/bin/clang -O2 -fobjc-arc -framework Cocoa -framework WebKit \
  "${HUB_DIR}/macos_app.m" -o "${MACOS_DIR}/SkillHub"
chmod +x "${MACOS_DIR}/SkillHub"

# 清理旧的外部二进制缓存
rm -rf "${HUB_DIR}/vault/bin"

# 4. Ad-hoc 签名并同步到 /Applications/Skill Hub.app
/usr/bin/codesign --force --deep --sign - "$APP_BUNDLE" 2>/dev/null || true
touch "$APP_BUNDLE"

if [ -d "/Applications" ] && [ -w "/Applications" ]; then
  rm -rf "/Applications/Skill Hub.app"
  cp -R "$APP_BUNDLE" "/Applications/Skill Hub.app"
  touch "/Applications/Skill Hub.app"
  /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f "/Applications/Skill Hub.app" 2>/dev/null || true
fi

echo "✅ Skill Hub.app 构建完成（已生成高清图标并同步至 /Applications/Skill Hub.app）"
