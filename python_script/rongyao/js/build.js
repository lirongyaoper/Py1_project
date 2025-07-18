/**
 * 资源构建和优化脚本
 * 用于压缩和合并CSS、JS文件
 */

const fs = require('fs');
const path = require('path');

// 配置
const config = {
    css: {
        input: [
            '{SITE_PATH}application/index/view/{C('site_theme')}/css/base.css',
            '{SITE_PATH}application/index/view/{C('site_theme')}/css/index.css',
            '{SITE_PATH}application/index/view/{C('site_theme')}/css/m.css'
        ],
        output: '{SITE_PATH}application/index/view/{C('site_theme')}/css/main.min.css'
    },
    js: {
        input: [
            '{SITE_PATH}application/index/view/{C('site_theme')}/js/common.js',
            '{SITE_PATH}application/index/view/{C('site_theme')}/js/js.js'
        ],
        output: '{SITE_PATH}application/index/view/{C('site_theme')}/js/main.min.js'
    }
};

// 简单的CSS压缩函数
function minifyCSS(css) {
    return css
        .replace(/\/\*[\s\S]*?\*\//g, '') // 删除注释
        .replace(/\s+/g, ' ') // 合并空白字符
        .replace(/\s*{\s*/g, '{') // 删除大括号周围的空白
        .replace(/\s*}\s*/g, '}') // 删除大括号周围的空白
        .replace(/\s*:\s*/g, ':') // 删除冒号周围的空白
        .replace(/\s*;\s*/g, ';') // 删除分号周围的空白
        .replace(/\s*,\s*/g, ',') // 删除逗号周围的空白
        .trim();
}

// 简单的JS压缩函数
function minifyJS(js) {
    return js
        .replace(/\/\*[\s\S]*?\*\//g, '') // 删除多行注释
        .replace(/\/\/.*$/gm, '') // 删除单行注释
        .replace(/\s+/g, ' ') // 合并空白字符
        .replace(/\s*{\s*/g, '{') // 删除大括号周围的空白
        .replace(/\s*}\s*/g, '}') // 删除大括号周围的空白
        .replace(/\s*;\s*/g, ';') // 删除分号周围的空白
        .replace(/\s*,\s*/g, ',') // 删除逗号周围的空白
        .trim();
}

// 合并文件
function mergeFiles(inputFiles, outputFile, minifyFunc) {
    let content = '';
    
    inputFiles.forEach(file => {
        if (fs.existsSync(file)) {
            content += fs.readFileSync(file, 'utf8') + '\n';
        } else {
            console.warn(`文件不存在: ${file}`);
        }
    });
    
    // 压缩内容
    const minified = minifyFunc(content);
    
    // 写入输出文件
    fs.writeFileSync(outputFile, minified);
    console.log(`已生成: ${outputFile}`);
}

// 主函数
function build() {
    console.log('开始构建资源文件...');
    
    // 合并CSS文件
    mergeFiles(config.css.input, config.css.output, minifyCSS);
    
    // 合并JS文件
    mergeFiles(config.js.input, config.js.output, minifyJS);
    
    console.log('构建完成！');
}

// 如果直接运行此脚本
if (require.main === module) {
    build();
}

module.exports = { build, minifyCSS, minifyJS }; 