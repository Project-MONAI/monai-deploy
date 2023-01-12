import http from 'k6/http';
import encoding from 'k6/encoding';
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

const credentials = `${__ENV.ORTHANC_USER}:${__ENV.ORTHANC_USER}`;
const url = __ENV.ORTHANC_URL;
const workflow_modality = config.orthanc.workflow_modality;
const no_workflow_modality = config.orthanc.workflow_modality;
const encodedCredentials = encoding.b64encode(credentials);
const lowerThinkTime = config.lowerThinkTime;
const upperThinkTime = config.upperThinkTime;
const ct_pacing = config.ct.pacing;
const mr_pacing = config.mr.pacing;
const us_pacing = config.us.pacing;
const rf_pacing = config.rf.pacing;

export function setup(){
  const ct = http.post(`${url}/tools/find`, JSON.stringify({
    "Level" : "Series",
    "Query" : {
        "Modality" : "CT"
    }
  }), set_request_header())

  const mr = http.post(`${url}/tools/find`, JSON.stringify({
    "Level" : "Series",
    "Query" : {
        "Modality" : "MR"
    }
  }), set_request_header())

  const us = http.post(`${url}/tools/find`, JSON.stringify({
    "Level" : "Series",
    "Query" : {
        "Modality" : "US"
    }
  }), set_request_header())

  let rf = http.post(`${url}/tools/find`, JSON.stringify({
    "Level" : "Series",
    "Query" : {
        "Modality" : "RF"
    }
  }), set_request_header())

  console.log(`Number of CT series available = ${ct.json().length}`)
  console.log(`Number of MR series available = ${mr.json().length}`)
  console.log(`Number of US series available = ${us.json().length}`)
  console.log(`Number of RF series available = ${rf.json().length}`)

  return {
    ct_data: ct.json(),
    mr_data: mr.json(),
    us_data: us.json(),
    rf_data: rf.json()
  }
}

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
      vus: config.ct.vus,
      iterations: config.ct.iterations,
      maxDuration: config.ct.maxDuration,
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
      vus: config.mr.vus,
      iterations: config.mr.iterations,
      maxDuration: config.mr.maxDuration,
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
      vus: config.us.vus,
      iterations: config.us.iterations,
      maxDuration: config.us.maxDuration,
    },
    rf_workflow: {
      executor: 'per-vu-iterations',
      exec: 'rf_workflow',
      vus: config.rf.vus,
      iterations: config.rf.iterations,
      maxDuration: config.rf.maxDuration,
    },
    rf_no_workflow: {
      executor: 'per-vu-iterations',
      exec: 'rf_no_workflow',
      vus: config.rf.vus,
      iterations: config.rf.iterations,
      maxDuration: config.rf.maxDuration,
    }
  },
};

export function ct_workflow(ct_data) {
  let ct_series_uids = ct_data["ct_data"]
  var startTime = Date.now();

  if(ct_series_uids.length > 0) {
    sleep(randomIntBetween(lowerThinkTime, upperThinkTime)); // think time
    let uid = ct_series_uids[Math.floor(Math.random() * ct_series_uids.length)];
    console.log(`Sending CT series with uid ${uid}`)
    let res = http.post(`${url}/modalities/${workflow_modality}/store`, get_request_body(uid), set_request_header(), { tags: { my_custom_tag: 'ct_workflow' } });
    check(res, {
      'is status 200': (r) => r.status === 200
    })
  } else
  {
    console.log("Series data does not exist for modality CT. Please check Orthanc")
  }

  sleep(pacing(ct_pacing, startTime));
}

export function ct_no_workflow() {
  let ct_series_uids = ct_data["ct_data"]
  var startTime = Date.now();

  if(ct_series_uids.length > 0) {
    sleep(randomIntBetween(lowerThinkTime, upperThinkTime)); // think time
    let uid = ct_series_uids[Math.floor(Math.random() * ct_series_uids.length)];
    console.log(`Sending CT series with uid ${uid}`)
    let res = http.post(`${url}/modalities/${no_workflow_modality}/store`, get_request_body(uid), set_request_header(), { tags: { my_custom_tag: 'ct_no_workflow' } });
    check(res, {
      'is status 200': (r) => r.status === 200
    })
  } else
  {
    console.log("Series data does not exist for modality CT. Please check Orthanc")
  }

  sleep(pacing(ct_pacing, startTime));
}

export function mr_workflow(mr_data) {
  let mr_series_uids = mr_data["mr_data"]
  var startTime = Date.now();

  if(mr_series_uids.length > 0) {
    sleep(randomIntBetween(lowerThinkTime, upperThinkTime)); // think time
    let uid = mr_series_uids[Math.floor(Math.random() * mr_series_uids.length)];
    console.log(`Sending MR series with uid ${uid}`)
    let res = http.post(`${url}/modalities/${workflow_modality}/store`, get_request_body(uid), set_request_header(), { tags: { my_custom_tag: 'mr_workflow' } });
    check(res, {
      'is status 200': (r) => r.status === 200
    })
  } else
  {
    console.log("Series data does not exist for modality MR. Please check Orthanc")
  }

  sleep(pacing(mr_pacing, startTime));
}

export function mr_no_workflow(mr_data) {
  let mr_series_uids = mr_data["mr_data"]
  var startTime = Date.now();

  if(mr_series_uids.length > 0) {
    sleep(randomIntBetween(lowerThinkTime, upperThinkTime)); // think time
    let uid = mr_series_uids[Math.floor(Math.random() * mr_series_uids.length)];
    console.log(`Sending MR series with uid ${uid}`)
    let res = http.post(`${url}/modalities/${no_workflow_modality}/store`, get_request_body(uid), set_request_header(), { tags: { my_custom_tag: 'mr_no_workflow' } });
    check(res, {
      'is status 200': (r) => r.status === 200
    })
  } else
  {
    console.log("Series data does not exist for modality MR. Please check Orthanc")
  }

  sleep(pacing(mr_pacing, startTime));
}

export function us_workflow(us_data) {
  let us_series_uids = us_data["us_data"]
  var startTime = Date.now();

  if(us_series_uids.length > 0) {
    sleep(randomIntBetween(lowerThinkTime, upperThinkTime)); // think time
    let uid = us_series_uids[Math.floor(Math.random() * us_series_uids.length)];
    console.log(`Sending US series with uid ${uid}`)
    let res = http.post(`${url}/modalities/${workflow_modality}/store`, get_request_body(uid), set_request_header(), { tags: { my_custom_tag: 'us_workflow' } });
    check(res, {
      'is status 200': (r) => r.status === 200
    })
  } else
  {
    console.log("Series data does not exist for modality US. Please check Orthanc")
  }

  sleep(pacing(us_pacing, startTime));
}

export function us_no_workflow(us_data) {
  let us_series_uids = us_data["us_data"]
  var startTime = Date.now();

  if(us_series_uids.length > 0) {
    sleep(randomIntBetween(lowerThinkTime, upperThinkTime)); // think time
    let uid = us_series_uids[Math.floor(Math.random() * us_series_uids.length)];
    console.log(`Sending US series with uid ${uid}`)
    let res = http.post(`${url}/modalities/${no_workflow_modality}/store`, get_request_body(uid), set_request_header(), { tags: { my_custom_tag: 'us_no_workflow' } });
    check(res, {
      'is status 200': (r) => r.status === 200
    })
  } else
  {
    console.log("Series data does not exist for modality US. Please check Orthanc")
  }

  sleep(pacing(us_pacing, startTime));
}

export function rf_workflow(rf_data) {
  let rf_series_uids = rf_data["rf_data"]
  var startTime = Date.now();

  if(rf_series_uids.length > 0) {
    sleep(randomIntBetween(lowerThinkTime, upperThinkTime)); // think time
    let uid = rf_series_uids[Math.floor(Math.random() * rf_series_uids.length)];
    console.log(`Sending RF series with uid ${uid}`)
    let res = http.post(`${url}/modalities/${workflow_modality}/store`, get_request_body(uid), set_request_header(), { tags: { my_custom_tag: 'rf_workflow' } });
    check(res, {
      'is status 200': (r) => r.status === 200
    })
  } else
  {
    console.log("Series data does not exist for modality RF. Please check Orthanc")
  }

  sleep(pacing(rf_pacing, startTime));
}

export function rf_no_workflow(rf_data) {
  let rf_series_uids = rf_data["rf_data"]
  var startTime = Date.now();

  if(rf_series_uids.length > 0) {
    sleep(randomIntBetween(lowerThinkTime, upperThinkTime)); // think time
    let uid = rf_series_uids[Math.floor(Math.random() * rf_series_uids.length)];
    console.log(`Sending RF series with uid ${uid}`)
    let res = http.post(`${url}/modalities/${no_workflow_modality}/store`, get_request_body(uid), set_request_header(), { tags: { my_custom_tag: 'rf_no_workflow' } });
    check(res, {
      'is status 200': (r) => r.status === 200
    })
  } else
  {
    console.log("Series data does not exist for modality RF. Please check Orthanc")
  }

  sleep(pacing(rf_pacing, startTime));
}

export function set_request_header(){
  return {
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Basic ${encodedCredentials}`,
    },
  };
};

export function get_request_body(uid){
  return JSON.stringify(    {
    "Resources": [`${uid}`]
  })
};

export function pacing(cycleTime, startTime) {
  let waitTime = 0;
  var endTime = Date.now();
  let duration = endTime - startTime;
  waitTime = cycleTime - duration;
  waitTime = waitTime / 1000;
  return waitTime;
}