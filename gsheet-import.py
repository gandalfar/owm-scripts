import requests

API_HOST = "http://oerworldmap.test/resource/"
AUTH_COOKIE = "0748b2e7-4036-4174-afa4-5eaa346e57b9"

MAGIC_HEADERS = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "content-type": "application/json",
    "Origin": API_HOST,
    "Referer": API_HOST,
    "Accept-Language": "en-US,en;q=0.9",
}

COOKIES = {
    "mod_auth_openidc_session": AUTH_COOKIE,
}


class Importer(object):
    def add_new_policy(self):
        data = {
            "@type": "Policy",
            "name": {"en": "Example policy fifteen"},
            "url": "http://example.com/policy2",
            "additionalType": [
                {
                    "@id": "https://oerworldmap.org/assets/json/policyTypes.json#policyDocument",
                    "@type": "Concept",
                }
            ],
            "description": {"en": "My english description"},
        }
        response = requests.post(
            "http://oerworldmap.test/resource/",
            headers=MAGIC_HEADERS,
            cookies=COOKIES,
            json=data,
            verify=False,
        )
        print(response.content)

    def update_policy(self):
        import requests

        cookies = {
            "mod_auth_openidc_session": "0748b2e7-4036-4174-afa4-5eaa346e57b9",
        }

        headers = {
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            "content-type": "application/json",
            "Origin": "http://oerworldmap.test",
            "Referer": "http://oerworldmap.test/resource/urn:uuid:c2e4df32-9131-4c12-b476-de6f4211da3a",
            "Accept-Language": "en-US,en;q=0.9",
        }

        data = {
            "additionalType": [
                {
                    "@id": "https://oerworldmap.org/assets/json/policyTypes.json#policyDocument",
                    "@type": "Concept",
                    "name": {
                        "pt": "Política",
                        "en": "Policy document",
                        "de": "Policy document",
                    },
                }
            ],
            "@type": "Policy",
            "name": {"en": "Example policy seventeen"},
            "@id": "urn:uuid:c2e4df32-9131-4c12-b476-de6f4211da3a",
            "@context": "https://oerworldmap.org/assets/json/context.json",
            "url": "http://example.com/policy2",
        }

        response = requests.post(
            "http://oerworldmap.test/resource/urn:uuid:c2e4df32-9131-4c12-b476-de6f4211da3a",
            headers=headers,
            cookies=cookies,
            json=data,
            verify=False,
        )


if __name__ == "__main__":
    imp = Importer()
    # imp.add_new_policy()
