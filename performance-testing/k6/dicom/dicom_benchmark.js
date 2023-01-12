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
const workflow_modality = config.orthanc.workflow_modality;
const encodedCredentials = encoding.b64encode(credentials);

export function setup(){
  const ct = http.post(`${url}/tools/find`, JSON.stringify({
    "Level" : "Series",
    "Query" : {
        "Modality" : "MR"
    }
  }), set_request_header())

  console.log(`Number of MR series available = ${ct.json().length}`)

  return {
    mr_data: ct.json()
  }
}

export const options = {
  scenarios: {
    mr_workflow: {
      executor: 'per-vu-iterations',
      exec: 'mr_workflow',
      vus: config.mr.vus,
      iterations: config.mr.iterations,
      maxDuration: config.mr.maxDuration,
    },
  },
};

export function mr_workflow(mr_data) {
  let mr_series_uids = mr_data["mr_data"]

  if(mr_series_uids.length > 0) {
    sleep(120)
    let uid = mr_series_uids[0];
    console.log(`Sending MR series with uid ${uid}`)
    let res = http.post(`${url}/modalities/${workflow_modality}/store`, get_request_body(uid), set_request_header(), { tags: { my_custom_tag: 'mr_workflow' } });
    check(res, {
      'is status 200': (r) => r.status === 200
    })
  } else
  {
    console.log("Series data does not exist for modality MR. Please check Orthanc")
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