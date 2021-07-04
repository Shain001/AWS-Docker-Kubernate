// var AWS = require('aws-sdk');
import AWS from 'aws-sdk'
import {
    ElMessage
} from 'element-plus'

// Set the region
// need to update the currentCredentials from AWS CLi (~/.aws/credentials)
// can not use Auth.currentCredentials() to get token because of the limitaion of account
AWS.config.update({
    accessKeyId: "ASIAZICFAFKEXVKJ3UHZ", // keyID
    secretAccessKey: "dso3RzVimML0YCWsP63k/2k/nJYcMFU1CW99NfrY", //secretAccessKey
    sessionToken: "FwoGZXIvYXdzENT//////////wEaDOENFO4vX3+eBQPshCLLARaOcGwkwITW2hMZjsKrDdF4sPXuQ6y7ZFOe+ofQr4xDVe7kdvMaIhCJp2rCZGO+h/Ubl9oJxID9MoP2IM6sFb516Afoz5pYZTUs06MEclKCbH8v1FFGmV9iHuMnOezdtuvnCsqRsuB65I0ffmd7qB+sqtCFhAtfOzKHfga1ODRSzY/84mIMYieCMLkv3qse0gCJ80mvtVyOcraeU/TB74Dc10wxhoqeMiv+8m73LF276VXKz7s42xWommy+7NQygyxow1icFSKuHjqdKPDl/oUGMi2VuYcC6EPuX2SSSklMOEpEFeimfxPFdXwVYYomfnRz/xHlLK/P/CzvDEdN9yE="
});
//create aws service
var s3 = new AWS.S3();
export function AwsUpdate(file) {
    var uploadParams = {
        Bucket: 'test-trigger-invoke',
        Key: file.name,
        Body: file, 
        "ACL": "public-read", 
        'Access-Control-Allow-Origin': '*'
    };
    var imgFile = new Promise(function (resolve) {
        s3.upload(uploadParams, function (err, data) {
            if (err) {
                console.log("Error", err);
                ElMessage.error('The provided token has expired, please rewrite image upload token in /src/utils/aws.js');
            }
            if (data) {
                resolve(data);
            }
        });
    });
    return imgFile
}