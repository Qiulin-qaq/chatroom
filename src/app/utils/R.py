class R:
    @staticmethod
    def ok(code=200,data=None, message='成功'):
        return {
            'code': code,
            'message': message,
            'data': data
        }

    @staticmethod
    def fail(code=400, data=None, message='失败'):
        return {
            'code': code,
            'message': message,
            'data': data
        }
