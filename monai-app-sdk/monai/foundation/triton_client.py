from tensorrtserver.api import ProtocolType, ServerHealthContext

class TritonClient:
    """
    Base class for connecting to TRITON server
    """
    
    def __init__(self):
        self.check_model_health()

    def check_model_health(self):
        """
        Checks readiness of TRITON and the model
        """
        protocol = ProtocolType.from_str(self.inference_config['inferer']['args']['protocol'])

        self.max_retry = 2 * 60 * 10 # about 10 minutes
        trial = 0
        while True:
            try:
                trial += 1
                health_context = ServerHealthContext(self.trtis_uri, protocol)
                self.logger.info("Trying to check TRTIS server health ...")
                if health_context.is_ready():
                    break
                raise ConnectionError
            except Exception as ex:
                if trial >= self.max_retry:
                    self.logger.exception('Failed to get server status'.format(ex))
                    raise
                else:
                    time.sleep(0.5)