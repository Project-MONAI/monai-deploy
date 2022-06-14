var express = require('express');
var router = express.Router();
var { storeScu } = require('dicom-dimse-native');

var options = {
  source: {
    aet: "DIMSE",
    ip: "127.0.0.1",
    port: 9999
  },
  target: {
    aet: "DIMSE",
    ip: "127.0.0.1",
    port: 4242
  },
  netTransferPropose: "1.2.840.10008.1.2.4.80",
  verbose: true
};

function randomlySelectDicom(scanType) {
  switch (scanType) {
    case "ct":
      return Math.floor(Math.random() * 5) + 1;
    case "mri":
      return Math.floor(Math.random() * 5) + 1;
    case "ultrasound":
      return Math.floor(Math.random() * 5) + 1;
    case "xray":
      return Math.floor(Math.random() * 5) + 1;
    default:
      console.log("Please select a valid scanType randomlySelectDicom method")
  }
}

function setSourcePath(scanType) {
  return options.sourcePath = "./dicom/" + scanType + "/" + randomlySelectDicom(scanType);
}

router.get('/ct', function (req, res, next) {
  setSourcePath("ct");
  storeScu(options, (result) => {
    console.log(JSON.parse(result));
  });
  res.status(200).send("Passed");
});

router.get('/mri', function (req, res, next) {
  setSourcePath("mri");
  storeScu(options, (result) => {
    console.log(JSON.parse(result));
  });
  res.status(200).send("Passed");
});

router.get('/ultrasound', function (req, res, next) {
  setSourcePath("ultrasound");
  storeScu(options, (result) => {
    console.log(JSON.parse(result));
  });
  res.status(200).send("Passed");
});

router.get('/xray', function (req, res, next) {
  setSourcePath("xray");
  storeScu(options, (result) => {
    console.log(JSON.parse(result));
  });
  res.status(200).send("Passed");
});

module.exports = router;
