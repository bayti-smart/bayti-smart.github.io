"""أدوات مشتركة لاستدعاء AliExpress API مع إعادة المحاولة عند تجاوز حد المعدّل."""
import time
import ae_sync as ae


def call_retry(method, params, tries=4):
    st, data = ae.call(method, params)
    for i in range(1, tries):
        err = data.get("error_response") if isinstance(data, dict) else None
        if err and err.get("code") in ("ApiCallLimit", "AppCallLimit"):
            time.sleep(3 * i)
            st, data = ae.call(method, params)
        else:
            break
    return st, data
