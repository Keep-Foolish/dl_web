const fs = require('fs');
const fs_extra = require('fs-extra');
const { spawn } = require('child_process');
const path = require("path");

function lodgingDetection(data_path, out_dir, name, sr) {
    fs.mkdirSync(`${out_dir}/${name.split(".")[0]}`, { recursive: true });
    fs.mkdirSync(`${data_path}/cutlist`, { recursive: true });
    fs.mkdirSync(`${data_path}/prelist`, { recursive: true });
    const pythonProcess = spawn('./dist/lodging_detection.exe', [data_path, out_dir, name, sr.toString()]); 

    // pythonProcess.stdout.on('data', (data) => {  
    //     console.log(data);
    // });
    
    pythonProcess.on('close', (code) => {  
        console.log(`child process exited with code ${code}`);
        // fs_extra.remove(`${data_path}/cutlist`);
        // fs_extra.remove(`${data_path}/prelist`);
    });
}

lodgingDetection("D:/3210613030/STD/UAV_ALD/lodging_detection/outfiles/input/", "D:/3210613030/STD/UAV_ALD/lodging_detection/outfiles/output/", "13.png", 234.4);

module.exports = { lodgingDetection };