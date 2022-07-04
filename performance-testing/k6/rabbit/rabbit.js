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
      exec: 'activeWorkflow',
      rate: config.activeWorkflow.rate,
      timeUnit: config.activeWorkflow.timeUnit, 
      duration: config.activeWorkflow.duration,
      preAllocatedVUs: config.activeWorkflow.preAllocatedVUs, 
    },
    mri: {
      executor: 'constant-arrival-rate',
      exec: 'inactiveWorkflow',
      rate: config.inactiveWorkflow.rate,
      timeUnit: config.inactiveWorkflow.timeUnit, 
      duration: config.inactiveWorkflow.duration,
      preAllocatedVUs: config.inactiveWorkflow.preAllocatedVUs, 
    },
  },
};

export function activeWorkflow() {
  http.get('http://localhost:5003/rabbit/activeworkflow', { tags: { my_custom_tag: 'activeWorkflow' } });
}

export function inactiveWorkflow() {
  http.get('http://localhost:5003/rabbit/inactiveworkflow', { tags: { my_custom_tag: 'inactiveWorkflow' } });
}
