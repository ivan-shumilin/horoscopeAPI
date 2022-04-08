from daily_horoscopes import views
from daily_horoscopes.serializers import ForecastSerializer
from daily_horoscopes.models import Forecast


from django.test import TestCase
import pdb, json


class ForecastSerializerTestCase(TestCase):
    fixtures = ['daily_horoscopes/tests/fixtures/forecast_test_serializers.json']

    def test_ok(self):
        queryset = Forecast.objects.all()
        data = ForecastSerializer(queryset, many=True).data
        expacted_data = [
            {
                "sing": "general",
                "description": "Сегодня день хорош для решительных перемен как в работе, так и в личной жизни. У Вас появится желание и возможность освободить свою жизнь от всего, что мешает душевному спокойствию: вредных привычек, зашедших в тупик отношений, грустных воспоминаний, неприятных обязанностей. Но все же, при принятии любых решений, Вы должны руководствоваться не эмоциями, а разумом. А иначе есть риск \"наломать много дров\" и совершить непоправимые ошибки. ",
                "date_create": "2022-04-05"
            },
            {
                "sing": "Овен",
                "description": "Сегодня Вас ждут незначительные финансовые потери предугадать которые было невозможно. В связи с этим событием Вас будут волновать вопросы материального характера. При встрече с любимым человеком, возможны серьезные осложнения отношений, вплоть до размолвки. Помогите окружающим и они будут помогать Вам. ",
                "date_create": "2022-04-05"
            },
            {
                "sing": "Телец",
                "description": "Сегодня очень хороший день, дает возможность изменить домашние условия к лучшему. Возможен переезд, получение квартиры, покупка дома или дачного участка, новой мебели и всяческих предметов комфорта, ремонт квартиры и т.д. В доме изобилие, которым Вы гордитесь, считая, что у Вас все лучшее, жена и дети тоже. А Вы дома всеми любимы и уважаемы. ",
                "date_create": "2022-04-05"
            }
        ]
        self.assertEqual(expacted_data, data)


