from datetime import datetime

from tests import TestCase

from stt.publish.stt_newsml_g2 import STTNewsmLG2Formatter


class STTNewsmlG2FormatterTestCase(TestCase):

    parse_source = False

    formatter = STTNewsmLG2Formatter()

    async def get_xml(self, article) -> str:
        output = await self.formatter.format(article, {})
        _, xml = output[0]
        assert xml
        print("XML", xml)
        return xml

    async def test_plaintext_public_ednote(self):
        article = {
            "profile": "nettiuutinen",
            "firstcreated": datetime.now(),
            "versioncreated": datetime.now(),
            "subject": [],
            "body_html": "<p>Test article body.</p>",
            "extra": {
                "sttpublicednote": "This is a plaintext ednote.",
            },
        }

        xml = await self.get_xml(article)
        assert "<p>This is a plaintext ednote.</p>" in xml

        article["profile"] = "foo"
        xml = await self.get_xml(article)
        assert (
            '<edNote role="sttnote:public">This is a plaintext ednote.</edNote>' in xml
        )
