import http from 'k6/http';

function getconfig() {
  try {
    return JSON.parse(open(__ENV.CONFIG));
  }
  catch (err) {
    throw new Error("Please set a config file using -e CONFIG=config/{appropriate-config-file}");
  }
}

let config = getconfig();

export const options = {
  discardResponseBodies: true,
  insecureSkipTLSVerify: true,
  scenarios: {
    ct: {
      executor: 'constant-arrival-rate',
      exec: 'ct',
      rate: config.ct.rate,
      timeUnit: config.ct.timeUnit, 
      duration: config.ct.duration,
      preAllocatedVUs: config.ct.preAllocatedVUs, 
    },
    mri: {
      executor: 'constant-arrival-rate',
      exec: 'mri',
      rate: config.mri.rate,
      timeUnit: config.mri.timeUnit, 
      duration: config.mri.duration,
      preAllocatedVUs: config.mri.preAllocatedVUs, 
    },
    ultrasound: {
      executor: 'constant-arrival-rate',
      exec: 'ultrasound',
      rate: config.ultrasound.rate,
      timeUnit: config.ultrasound.timeUnit, 
      duration: config.ultrasound.duration,
      preAllocatedVUs: config.ultrasound.preAllocatedVUs, 
    },
    xray: {
      executor: 'constant-arrival-rate',
      exec: 'xray',
      rate: config.xray.rate,
      timeUnit: config.xray.timeUnit, 
      duration: config.xray.duration,
      preAllocatedVUs: config.xray.preAllocatedVUs, 
    },
  },
};

export function ct() {
  http.get('http://localhost:5003/dicom/ct', { tags: { my_custom_tag: 'ct' } });
}

export function mri() {
  http.get('http://localhost:5003/dicom/mri', { tags: { my_custom_tag: 'mri' } });
}

export function ultrasound() {
  http.get('http://localhost:5003/dicom/ultrasound', { tags: { my_custom_tag: 'ultrasound' } });
}

export function xray() {
  http.get('http://localhost:5003/dicom/xray', { tags: { my_custom_tag: 'xray' } });
}