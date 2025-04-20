import GeoTIFF from 'geotiff';
import { createCanvas, loadImage } from 'canvas';
import fs from 'fs';

// 计算空间分辨率（每像素面积）函数
async function calculateSR(tifPath) {
    const tiff = await GeoTIFF.fromFile(tifPath);
    const image = await tiff.getImage();
    const transform = image.getGeoTransform();
    const crs = image.getCRS();
    const width = image.getWidth();
    const height = image.getHeight();
    console.log(`图像坐标参考系统（CRS）：${crs}`);

    // 获取图像中心的地理坐标
    const centerX = transform[2] + (width / 2) * transform[0]; // X轴中心
    const centerY = transform[5] + (height / 2) * transform[4]; // Y轴中心
    console.log(`图像中心的地理坐标（X, Y）：(${centerX}, ${centerY})`);

    // 使用图像中心的纬度进行每像素面积的计算
    const pixelWidth = transform[0]; // 经度方向的像素大小
    const pixelHeight = transform[4]; // 纬度方向的像素大小（负值）

    // 计算中心纬度的弧度值
    const latitudeRad = Math.radians(centerY);

    // 计算像素宽度和高度的实际地面尺寸（单位：米）
    const pixelWidthInMeters = Math.abs(pixelWidth) * 111320 * Math.cos(latitudeRad);
    const pixelHeightInMeters = Math.abs(pixelHeight) * 111320; // 每度纬度大约是 111320 米

    // 每个像素的面积（平方米）
    const sr = pixelWidthInMeters * pixelHeightInMeters;
    console.log(`空间分辨率（每像素面积）：${sr.toFixed(4)} 平方米`);

    return sr;
}

// 统计每种颜色像素数量并计算面积
async function calculateAreaFromSegmentation(segImagePath, pixelArea) {
    const image = await loadImage(segImagePath);
    const canvas = createCanvas(image.width, image.height);
    const ctx = canvas.getContext('2d');
    ctx.drawImage(image, 0, 0);

    const imageData = ctx.getImageData(0, 0, image.width, image.height);
    const data = imageData.data;

    // 定义颜色标签
    const redLabel = { r: 250, g: 4, b: 27 };     // 倒伏
    const greenLabel = { r: 4, g: 250, b: 27 };   // 未倒伏
    const blackLabel = { r: 0, g: 0, b: 0 };      // 背景

    let redCount = 0, greenCount = 0, blackCount = 0;

    // 遍历图像像素
    for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];

        if (r === redLabel.r && g === redLabel.g && b === redLabel.b) {
            redCount++;
        } else if (r === greenLabel.r && g === greenLabel.g && b === greenLabel.b) {
            greenCount++;
        } else if (r === blackLabel.r && g === blackLabel.g && b === blackLabel.b) {
            blackCount++;
        }
    }

    // 计算每种区域的面积
    const redArea = redCount * pixelArea;
    const greenArea = greenCount * pixelArea;
    const blackArea = blackCount * pixelArea;

    console.log(`倒伏区域（红）面积：${redArea.toFixed(2)} 平方米`);
    console.log(`未倒伏区域（绿）面积：${greenArea.toFixed(2)} 平方米`);
    console.log(`背景区域（黑）面积：${blackArea.toFixed(2)} 平方米`);
    console.log(`图像总面积：${(redArea + greenArea + blackArea).toFixed(2)} 平方米`);

    return { redArea, greenArea, blackArea };
}

// 主程序
(async function() {
    const tifPath = 'C:/Users/zhangwei/Desktop/小麦倒伏数据/tif/20210531-field2.tif';
    const segImagePath = 'C:/Users/zhangwei/Desktop/result/20210531-field2-annoted/20210531-field2-annoted.png';

    try {
        const pixelArea = await calculateSR(tifPath);
        await calculateAreaFromSegmentation(segImagePath, pixelArea);
    } catch (error) {
        console.error('发生错误：', error);
    }
})();
