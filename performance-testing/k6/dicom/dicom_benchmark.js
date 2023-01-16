import http from 'k6/http';
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

const url = __ENV.URL;
const dicom_modality = __ENV.DICOM_MODALITY
const workflow_AET = config.remote_modalities.workflow_AET;

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

export function benchmark_workflow() {

  let res = http.get(`${url}/dicom?modality=${dicom_modality}&AET=${workflow_AET}`, { tags: { my_custom_tag: 'benchmark_workflow' } })

  check(res, {
    'is status 200': (r) => r.status === 200
  })

  sleep(60);
}

export function set_request_header(){
  return {
    headers: {
        'Content-Type': 'application/json'
    },
  };
};