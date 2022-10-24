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

const credentials = `${config.orthanc.username}:${config.orthanc.password}`;
const url = config.orthanc.url;
const workflow_modality = config.orthanc.workflow_modality;
const encodedCredentials = encoding.b64encode(credentials);
const liver_ct = config.orthanc.liver_ct;

export const options = {
  scenarios: {
    mr_workflow: {
      executor: 'per-vu-iterations',
      exec: 'ct_workflow',
      vus: config.ct.vus,
      iterations: config.ct.iterations,
      maxDuration: config.ct.maxDuration,
    },
  },
};

export function ct_workflow() {
  sleep(120)
  let res = http.post(`${url}/modalities/${workflow_modality}/store`, get_request_body(liver_ct), set_request_header(), { tags: { my_custom_tag: 'liver_seg' } });
  check(res, {
    'is status 200': (r) => r.status === 200
  })
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