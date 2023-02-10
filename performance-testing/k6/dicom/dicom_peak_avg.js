import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomIntBetween } from "https://jslib.k6.io/k6-utils/1.1.0/index.js";

function getconfig() {
  try {
    return JSON.parse(open(__ENV.CONFIG));
  }
  catch (err) {
    throw new Error("Please set a config file using -e CONFIG=config/{appropriate-config-file}");
  }
}

let config = getconfig();

const url = __ENV.URL;
const workflow_AET = __ENV.WF_AET;
const no_workflow_AET = __ENV.NO_WF_AET;
const ct_pacing = config.ct.pacing;
const ct_no_pacing = config.ct_no.pacing
const mr_pacing = config.mr.pacing;
const mr_no_pacing = config.mr_no.pacing
const us_pacing = config.us.pacing;
const us_no_pacing = config.us_no.pacing
const rf_pacing = config.rf.pacing;

export const options = {
  scenarios: {
    ct_workflow: {
      executor: 'per-vu-iterations',
      exec: 'ct_workflow',
      vus: config.ct.vus,
      iterations: config.ct.iterations,
      maxDuration: config.ct.maxDuration,
    },
    ct_no_workflow: {
      executor: 'per-vu-iterations',
      exec: 'ct_workflow',
      vus: config.ct_no.vus,
      iterations: config.ct_no.iterations,
      maxDuration: config.ct_no.maxDuration,
    },
    mr_workflow: {
      executor: 'per-vu-iterations',
      exec: 'mr_workflow',
      vus: config.mr.vus,
      iterations: config.mr.iterations,
      maxDuration: config.mr.maxDuration,
    },
    mr_no_workflow: {
      executor: 'per-vu-iterations',
      exec: 'mr_no_workflow',
      vus: config.mr_no.vus,
      iterations: config.mr_no.iterations,
      maxDuration: config.mr_no.maxDuration,
    },
    us_workflow: {
      executor: 'per-vu-iterations',
      exec: 'us_workflow',
      vus: config.us.vus,
      iterations: config.us.iterations,
      maxDuration: config.us.maxDuration,
    },
    us_no_workflow: {
      executor: 'per-vu-iterations',
      exec: 'us_no_workflow',
      vus: config.us_no.vus,
      iterations: config.us_no.iterations,
      maxDuration: config.us_no.maxDuration,
    },
    rf_workflow: {
      executor: 'per-vu-iterations',
      exec: 'rf_workflow',
      vus: config.rf.vus,
      iterations: config.rf.iterations,
      maxDuration: config.rf.maxDuration,
    }
  },
};

export function ct_workflow() {
  var startTime = Date.now();
  sleep(randomIntBetween(lowerThinkTime, upperThinkTime)); // think time
  let res = http.get(`${url}/dicom?modality=CT&CalledAET=${workflow_AET}&CallingAET=${workflow_AET}`, { tags: { my_custom_tag: 'ct_workflow' } })
  check(res, {
    'is status 200': (r) => r.status === 200
  })
  sleep(pacing(ct_pacing, startTime));
}

export function ct_no_workflow() {
  var startTime = Date.now();
  let res = http.get(`${url}/dicom?modality=CT&CalledAET=${no_workflow_AET}&CallingAET=${no_workflow_AET}`, { tags: { my_custom_tag: 'ct_no_workflow' } })
  check(res, {
    'is status 200': (r) => r.status === 200
  })
  sleep(pacing(ct_no_pacing, startTime));
}

export function mr_workflow() {
  var startTime = Date.now();
  let res = http.get(`${url}/dicom?modality=MR&CalledAET=${workflow_AET}&CallingAET=${workflow_AET}`, { tags: { my_custom_tag: 'mr_workflow' } })
  check(res, {
    'is status 200': (r) => r.status === 200
  })
  sleep(pacing(mr_pacing, startTime));
}

export function mr_no_workflow() {
  var startTime = Date.now();
  let res = http.get(`${url}/dicom?modality=MR&CalledAET=${no_workflow_AET}&CallingAET=${no_workflow_AET}`, { tags: { my_custom_tag: 'mr_no_workflow' } })
  check(res, {
    'is status 200': (r) => r.status === 200
  })
  sleep(pacing(mr_no_pacing, startTime));
}

export function us_workflow() {
  var startTime = Date.now();
  let res = http.get(`${url}/dicom?modality=US&CalledAET=${workflow_AET}&CallingAET=${workflow_AET}`, { tags: { my_custom_tag: 'us_workflow' } })
  check(res, {
    'is status 200': (r) => r.status === 200
  })
  sleep(pacing(us_pacing, startTime));
}

export function us_no_workflow() {
  var startTime = Date.now();
  let res = http.get(`${url}/dicom?modality=US&CalledAET=${no_workflow_AET}&CallingAET=${no_workflow_AET}`, { tags: { my_custom_tag: 'us_no_workflow' } })
  check(res, {
    'is status 200': (r) => r.status === 200
  })
  sleep(pacing(us_no_pacing, startTime));
}

export function rf_workflow() {
  var startTime = Date.now();
  let res = http.get(`${url}/dicom?modality=RF&CalledAET=${workflow_AET}&CallingAET=${workflow_AET}`, { tags: { my_custom_tag: 'rf_workflow' } })
  check(res, {
    'is status 200': (r) => r.status === 200
  })
  sleep(pacing(rf_pacing, startTime));
}

export function set_request_header(){
  return {
    headers: {
        'Content-Type': 'application/json'
    },
  };
};

export function pacing(cycleTime, startTime) {
  let waitTime = 0;
  var endTime = Date.now();
  let duration = endTime - startTime;
  waitTime = Math.round(cycleTime - (duration/1000));
  return waitTime
}