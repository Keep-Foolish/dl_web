import GeoTIFF from 'geotiff';

async function calculate_sr(tifFile) {
    const arrayBuffer = await tifFile.arrayBuffer();
    const tiff = await GeoTIFF.fromArrayBuffer(arrayBuffer);
    const image = await tiff.getImage();

    const transform = image.getGeoKeys().ModelTransformation || image.getTiePoints()[0];
    const width = image.getWidth();
    const height = image.getHeight();
    const crs = image.getGeoKeys().ProjectedCSTypeGeoKey;

    console.log("图像坐标参考系统（CRS）：", crs);

    const latitude = 30.0;
    const latitude_rad = latitude * Math.PI / 180;

    const pixelWidth = image.getResolution()[0];  // 注意这里可能需要自查 getResolution() 返回值单位
    const pixelHeight = image.getResolution()[1];

    const pixel_width_in_meters = Math.abs(pixelWidth) * 111320 * Math.cos(latitude_rad);
    const pixel_height_in_meters = Math.abs(pixelHeight) * 111320;

    const sr = pixel_width_in_meters * pixel_height_in_meters;
    console.log(`空间分辨率（每像素面积）：${sr.toFixed(4)} 平方米`);
    return sr;
}


function calculate_area_from_segmentation(imageElement, pixelArea) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    canvas.width = imageElement.width;
    canvas.height = imageElement.height;

    ctx.drawImage(imageElement, 0, 0);
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    const redLabel = [250, 4, 27];
    const greenLabel = [4, 250, 27];
    const blackLabel = [0, 0, 0];

    let redCount = 0;
    let greenCount = 0;
    let blackCount = 0;

    for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];

        if (r === redLabel[0] && g === redLabel[1] && b === redLabel[2]) {
            redCount++;
        } else if (r === greenLabel[0] && g === greenLabel[1] && b === greenLabel[2]) {
            greenCount++;
        } else if (r === blackLabel[0] && g === blackLabel[1] && b === blackLabel[2]) {
            blackCount++;
        }
    }

    const redArea = redCount * pixelArea;
    const greenArea = greenCount * pixelArea;
    const blackArea = blackCount * pixelArea;

    console.log(`倒伏区域（红）面积：${redArea.toFixed(2)} 平方米`);
    console.log(`未倒伏区域（绿）面积：${greenArea.toFixed(2)} 平方米`);
    console.log(`背景区域（黑）面积：${blackArea.toFixed(2)} 平方米`);
    console.log(`图像总面积：${(redArea + greenArea + blackArea).toFixed(2)} 平方米`);

    return { redArea, greenArea, blackArea };
}

export { calculate_sr, calculate_area_from_segmentation }