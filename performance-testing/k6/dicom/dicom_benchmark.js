import http from 'k6/http';
import encoding from 'k6/encoding';
import { check, sleep } from 'k6';

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
const dicom_modality = __ENV.DICOM_MODALITY
const workflow_modality = config.orthanc.workflow_modality;
const encodedCredentials = encoding.b64encode(credentials);

export function setup(){
  const dicom = http.post(`${url}/tools/find`, JSON.stringify({
    "Level" : "Series",
    "Query" : {
        "Modality" : `${__ENV.DICOM_MODALITY}`
    }
  }), set_request_header())

  console.log(`Number of ${__ENV.DICOM_MODALITY} series available = ${dicom.json().length}`)

  return {
    dicom_data: dicom.json()
  }
}

export const options = {
  scenarios: {
    benchmark_workflow: {
      executor: 'per-vu-iterations',
      exec: 'benchmark_workflow',
      vus: config.benchmark.vus,
      iterations: config.benchmark.iterations,
      maxDuration: config.benchmark.maxDuration,
    },
  },
};

export function benchmark_workflow(dicom_data) {
  let dicom_series_uids = dicom_data["dicom_data"]

  if(dicom_series_uids.length > 0) {
    sleep(120)
    let uid = dicom_series_uids[Math.floor(Math.random() * dicom_series_uids.length)];
    console.log(`Sending ${__ENV.DICOM_MODALITY} series with uid ${uid}`)
    let res = http.post(`${url}/modalities/${workflow_modality}/store`, get_request_body(uid), set_request_header(), { tags: { my_custom_tag: 'benchmark_workflow' } });
    check(res, {
      'is status 200': (r) => r.status === 200
    })
  } else
  {
    console.log(`Series data does not exist for modality ${__ENV.DICOM_MODALITY}. Please check Orthanc`)
  }
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