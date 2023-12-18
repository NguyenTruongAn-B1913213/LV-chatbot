# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import spacy
from datetime import datetime, timedelta
import requests
import random
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class GetWeatherAction(Action):
    def name(self):
        return "action_get_weather"

    def run(self, dispatcher, tracker, domain):
        response = requests.get("http://localhost:3000/api/get-bacsi")
        data = response.json()  # Giả sử API trả về một danh sách bác sĩ dưới dạng JSON
        buttons = []
        for doctor in data:
            button = {
                "title": doctor["tenBS"],  # Tên bác sĩ
                # "payload": f"/select_doctor{{'doctor_id': {doctor['_id']}}}",  # Payload để xác định bác sĩ được chọn
                "payload": doctor['_id'],
            }
            print(button)
            buttons.append(button)
        dispatcher.utter_button_message(text="Danh sách bác sĩ:", buttons=buttons)
        return []

class ActionScheduleAppointment(Action):
    def name(self):
        return "action_schedule_appointment"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        # Extract relevant slot values from the tracker
#         user_id = tracker.get_slot(
#         user_id = tracker.get
# "user_id")
#         id_bs = tracker.get_slot(
#         id_bs
# "id_bs")
#         ngaygio_kham = tracker.get_slot(
#         ngay
# "ngaygio_kham")
#         madinhdanh = tracker.get_slot(
#         madinhdanh = tracker.get_slot
# "madinhdanh")
#         ten = tracker.get_slot(
#         ten = tracker.get_slot

#         ten =
# "ten")
#         ngay_sinh = tracker.get_slot(
#         ngay_sinh = tracker.get
# "ngay_sinh")
#         gioi_tinh = tracker.get_slot("gioi_tinh")
#         dia_chi = tracker.get_slot("dia_chi")
#         so_dien_thoai = tracker.get_slot("so_dien_thoai")
#         trieuchung = tracker.get_slot("trieuchung")

        # Define the API endpoint for appointment scheduling
        api_url = "http://localhost:3000/api/lichkham"

        # Prepare the data to send to the API
        data = {
            "idBS": '651e4932da8cd0ce3c205f76',
            "ngaygioKham": { "thu": 'Thứ Hai', "ca": 'Sáng' },
            "madinhdanh": '121232123213',
            "ten": 'saasdsad',
            "ngaySinh": '2023-09-26',
            "gioiTinh": 'Nam',
            "diaChi": 'sadsadsaddsasa',
            "soDienThoai": 'asdsaasdsadsad',
            "trieuchung": 'ho benh'
        }
        print(data)
        try:
            # Make a POST request to the API to schedule the appointment
            api_response = requests.post(api_url, json=data)
            print(api_response)
            if api_response.status_code == 200:
                dispatcher.utter_message("Lịch hẹn của bạn đã được đặt thành công.")
            else:
                dispatcher.utter_message("Đã xảy ra lỗi trong quá trình đặt lịch. Vui lòng thử lại sau.")
        except Exception as e:
            # Handle any exceptions that may occur during the API request
            dispatcher.utter_message("Có lỗi xảy ra khi thực hiện đặt lịch. Vui lòng thử lại sau.")

        return []
    


# ở trên tim hiểu lại

class ActionDatLich(Action):
    def name(self):
        return "action_dat_lich"

    def run(self, dispatcher, tracker, domain):
        appointment_url = "http://localhost:8080/DatLichKham"
        dispatcher.utter_message(f"Bạn vui lòng truy cập vào link sau: <a href='{appointment_url}'>{appointment_url}</a> và điền đầy đủ thông tin để đặt lịch khám")
        return []
class ask_name_appointment(Action):
    def name(self):
        return "ask_name_appointment"

    def run(self, dispatcher, tracker, domain):
        name = next(tracker.get_latest_entity_values("name"), None)
        bs = next(tracker.get_latest_entity_values("bs"), None)
        intent = tracker.latest_message['intent'].get('name')
        appointment_url = "http://localhost:8080/DatLichKham"
        if name and intent =="ask_name_appointment":
         response = f"Xin chào, {name}. Giờ làm việc của phòng khám: sáng(6h - 7h40) Trưa(11h-13h) chiều(5h - 8h40) Thứ 2 - Chủ Nhật. Bạn vui lòng truy cập vào<a href='{appointment_url}'>{appointment_url}</a>"
        else:
            response = "Tôi không hiểu ý kiến của bạn và bạn vui lòng tóm tắt lại ý trên"
        dispatcher.utter_message(response)
        return []

class ask_name(Action):
    def name(self):
        return "ask_name"

    def run(self, dispatcher, tracker, domain):
        name = next(tracker.get_latest_entity_values("name"), None)
        print(name)
        intent = tracker.latest_message['intent'].get('name')
        if name and intent=="ask_name" :
         response = f"Xin chào {name} ,Bạn có thể yêu cầu tôi hỗ trợ gì ạ!,"
        else:
            response = "Tôi không hiểu ý kiến của bạn và bạn vui lòng tóm tắt lại ý trên"
        dispatcher.utter_message(response)
        return []

from datetime import datetime, timedelta

class YeuCauLichHen(Action):
    def name(self):
        return "yêu_cầu_lịch_hẹn_co_thời_gian"
    def get_weekday_name(self, weekday_number):
        days_mapping = {"thứ 2": 0, "thứ 3": 1, "thứ 4": 2, "thứ 5": 3, "thứ 6": 4, "thứ 7": 5, "chủ nhật": 6}
        for key, value in days_mapping.items():
            if value == weekday_number:
                return key
        return "unknown"
    def run(self, dispatcher, tracker, domain):
        current_date = datetime.now()
        response = ""
        thu = next(tracker.get_latest_entity_values("thu"), None)
        ca = next(tracker.get_latest_entity_values("ca"), None)
        appointment_url = "http://localhost:8080/DatLichKham"
        doctors_with_desired_working_day = []
        # Map the days to their corresponding weekday numbers
        days_mapping = {"thứ 2": 0, "thứ 3": 1, "thứ 4": 2, "thứ 5": 3, "thứ 6": 4, "thứ 7": 5, "chủ nhật": 6}

        if thu and thu.lower() in days_mapping and ca is None:
            target_weekday = days_mapping[thu.lower()]
            days_to_add = target_weekday - current_date.weekday() if target_weekday >= current_date.weekday() else 7 - current_date.weekday() + target_weekday
            if target_weekday == current_date.weekday():
                days_to_add += 7
            next_occurrence = current_date + timedelta(days=days_to_add)
            responseTime = requests.get(f'http://localhost:3000/api/get-datework')
            responseTime.raise_for_status() 
            schedule_list = responseTime.json()
            responseDoctor = requests.get(f'http://localhost:3000/api/get-bacsi')
            responseDoctor.raise_for_status()
            Doctor_list = responseDoctor.json()
            desired_working_hour_id = None
            for item in schedule_list:
                if item['thu'].lower() == thu:
                    desired_working_hour_id = item['_id']
                    break
            print(desired_working_hour_id)
            for doctor in Doctor_list:
                for working_day_id in doctor.get('ngayLamViec', []):
                    if working_day_id ==desired_working_hour_id:
                        doctors_with_desired_working_day.append(doctor)
            if doctors_with_desired_working_day:
                doctor_info = "\n".join([f"- {doctor['tenBS']} ({doctor['chuyenKhoa']})" for doctor in doctors_with_desired_working_day])
                response += f"\n\nDanh sách bác sĩ có lịch làm việc vào thời điểm này:\n{doctor_info} Bạn vui lòng điền vào link<a href='{appointment_url}'>{appointment_url}</a> để thực hiện đặt lịch khám. "
                dispatcher.utter_message(response)
                return []
        elif thu and thu.lower() in days_mapping and ca:
            target_weekday = days_mapping[thu.lower()]
            days_to_add = target_weekday - current_date.weekday() if target_weekday >= current_date.weekday() else 7 - current_date.weekday() + target_weekday
            if target_weekday == current_date.weekday():
                days_to_add += 7
            print(1)
            next_occurrence = current_date + timedelta(days=days_to_add)
            responseTime = requests.get(f'http://localhost:3000/api/get-datework')
            responseDoctor = requests.get(f'http://localhost:3000/api/get-bacsi')
            responseDoctor.raise_for_status()
            responseTime.raise_for_status() 
            schedule_list = responseTime.json()
            Doctor_list = responseDoctor.json()
            desired_working_hour_id = None
            print(2)
            for item in schedule_list:
                if item['thu'].lower() == thu and item['ca'].lower() == ca:
                    desired_working_hour_id = item['_id']
                    break
            print(desired_working_hour_id)
            print("----------------")
            doctors_with_desired_working_day = []
            for doctor in Doctor_list:
                for working_day_id in doctor.get('ngayLamViec', []):
                
                    print(working_day_id)
                    if working_day_id ==desired_working_hour_id:
                        print(doctor)
                        doctors_with_desired_working_day.append(doctor)
            print(doctors_with_desired_working_day)
            if doctors_with_desired_working_day:
                doctor_info = "\n".join([f"- {doctor['tenBS']} ({doctor['chuyenKhoa']})" for doctor in doctors_with_desired_working_day])

                response += f"\n\nDanh sách bác sĩ có lịch làm việc vào thời điểm này:\n{doctor_info} Bạn vui lòng điền vào link {appointment_url} để thực hiện đặt lịch khám. "
                print(response)
                dispatcher.utter_message(response)
                return []
        elif thu.lower() == "ngày mai":
            next_day = current_date + timedelta(days=1)
            next_day_name = self.get_weekday_name(next_day.weekday())
            responseTime = requests.get(f'http://localhost:3000/api/get-datework')
            responseDoctor = requests.get(f'http://localhost:3000/api/get-bacsi')
            responseDoctor.raise_for_status()
            responseTime.raise_for_status() 
            schedule_list = responseTime.json()
            Doctor_list = responseDoctor.json()
            desired_working_hour_id = None
            print(thu)
            for item in schedule_list:
                if item['thu'].lower() == next_day_name and item['ca'].lower() == ca:
                    desired_working_hour_id = item['_id']
                    break
            for doctor in Doctor_list:
                for working_day_id in doctor.get('ngayLamViec', []):
                    if working_day_id == desired_working_hour_id:
                        doctors_with_desired_working_day.append(doctor)
            if doctors_with_desired_working_day:
                doctor_info = "\n".join([f"- {doctor['tenBS']} ({doctor['chuyenKhoa']})" for doctor in doctors_with_desired_working_day])
                response += f"\n\nDanh sách bác sĩ có lịch làm việc vào thời điểm này:\n{doctor_info} Bạn vui lòng điền vào link {appointment_url} để thực hiện đặt lịch khám."
                dispatcher.utter_message(response)
                return []
            else:
                response = "Không có bác sĩ nào làm việc vào ngày này bạn vui lòng chọn ngày khác."
                dispatcher.utter_message(response)
        else:
            response = "Tôi không hiểu ý kiến của bạn và bạn vui lòng tóm tắt lại ý trên."
        dispatcher.utter_message(response)
        return []


# BS
class AskNameAppointment(Action):
    def name(self):
        return "appointment_bs"

    def run(self, dispatcher, tracker, domain):
        bs = next(tracker.get_latest_entity_values("bacsi"), None)
        if bs:
            response = requests.get(f'http://localhost:3000/api/getName-bacsi/{bs}')
            doctor_data = response.json()
            doctor_name = doctor_data.get("tenBS", None)
            appointment_url = "http://localhost:8080/DatLichKham"
            if doctor_name:
                res = f"Xin chào Bạn, Bạn muốn Đặt lịch với bác sĩ {doctor_name} bạn vui lòng truy cập vào <a href='{appointment_url}'>{appointment_url}</a> và thực hiện theo yêu cầu để thực hiện đặt lịch khám."
            else:
                res = "Tôi không thể tìm thấy tên bác sĩ trong phòng khám hoặc sai tên bác sĩ. Bạn vui lòng kiểm tra lại."
        else:
            res = "Tôi không hiểu ý kiến của bạn và bạn vui lòng tóm tắt lại ý trên."

        dispatcher.utter_message(res)
        return []
import requests

from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class DoctorTime(Action):
    def name(self):
        return "DoctorTime"

    def run(self, dispatcher, tracker, domain):
        bs = next(tracker.get_latest_entity_values("bacsi"), None)
        name = next(tracker.get_latest_entity_values("name"), None)
        appointment_url = "http://localhost:8080/DatLichKham"
        
        if bs:
            response = requests.get(f'http://localhost:3000/api/getName-bacsi/{bs}')
            response.raise_for_status()  # Raise an exception for unsuccessful responses
            
            responseTime = requests.get(f'http://localhost:3000/api/get-datework')
            responseTime.raise_for_status()  # Raise an exception for unsuccessful responses

            doctor_data = response.json()
            ngay_lam_viec = doctor_data.get('ngayLamViec', [])  # Check if 'ngayLamViec' exists
            schedule_list = responseTime.json()
            matched_dicts = [schedule_dict for schedule_dict in schedule_list if schedule_dict["_id"] in ngay_lam_viec]
            print(matched_dicts)
            doctor_name = doctor_data.get("tenBS", None)
            
            if doctor_name:
                schedule_rows = [
                    f"<tr><td>{schedule['thu']}</td><td>({schedule['ca']})</td><td>{schedule['gioBatDau']} - {schedule['gioKetThuc']}</td></tr>"
                    for schedule in matched_dicts
                ]
                schedule_table = "<table class='table table-bordered table-striped table-borderless table-hover' style='font-size: 18px;width: 100%;'><tr><th style='text-align: left'>Thứ</th><th>Ca</th><th>Thời Gian</th></tr>" + "\n".join(schedule_rows) + "</table>"
                
                # Kiểm tra xem `name` có giá trị hay không trước khi sử dụng
                if name:
                    res = f"Xin chào {name}, Thời gian làm việc của bác sĩ {doctor_name} là:\n{schedule_table}\nBạn vui lòng truy cập vào <a href='{appointment_url}'>{appointment_url}</a> đầy đủ thông tin bệnh nhân để thực hiện đặt lịch khám với phòng khám của chúng tôi."
                else:
                    res = f"Thời gian làm việc của bác sĩ {doctor_name} là:\n{schedule_table}\nBạn vui lòng truy cập vào <a href='{appointment_url}'>{appointment_url}</a> đầy đủ thông tin bệnh nhân để thực hiện đặt lịch khám với phòng khám của chúng tôi."
            else:
                res = "Tôi không thể tìm thấy tên bác sĩ trong phòng khám hoặc sai tên bác sĩ. Bạn vui lòng kiểm tra lại."
        else:
            res = "Tôi không hiểu ý kiến của bạn và bạn vui lòng tóm tắt lại ý trên."

        dispatcher.utter_message(res, useHTML=True)
        return [SlotSet("name", name)]



class greet(Action):
    def name(self):
        return "greet"

    def run(self, dispatcher, tracker, domain):
        # Get entities from the user's input
        intent = tracker.latest_message['intent'].get('name')
        print(intent)
        greet_responses = [
            "Xin chào Bạn, Bạn có thể vui lòng cho tôi biết tên được không ạ!",
            "Xin chào Bạn, đã đến với phòng khám chúng tôi bạn có thể vui lòng cho tôi biết tên được không ạ!",
            "Xin chào bạn đã đến với phòng khám chúng tôi, tôi có thế giúp gì cho bạn ạ!",
            "Xin chào bạn đã đến với phòng khám chúng tôi, chúc bạn một ngày vui",
        ]
        # Check if there are any entities
        if intent == "greet":
            # If there are entities, perform the necessary actions
            # (you can customize this part based on your use case)
            res = random.choice(greet_responses)
            dispatcher.utter_message(res)
        else:
            # If there are no entities, respond with a default message
            res = "Tôi không hiểu ý định bạn như thế nào."
            dispatcher.utter_message(res)

        # You can also set slots or perform other actions based on the entities
        # or the absence of entities using SlotSet or other events if needed
        # For example:
        # dispatcher.utter_message(response="utter_greet", custom_slot="value")
        # return [SlotSet("some_slot", "some_value")]

        
        return []
class greet(Action):
    def name(self):
        return "Thank"

    def run(self, dispatcher, tracker, domain):
        # Get entities from the user's input
        intent = tracker.latest_message['intent'].get('name')
        print(intent)
        thank_responses = [
            "Tôi rất hân dự được phục vụ bạn.",
            "Tôi thật hạnh phúc được phục vụ bạn.",
            "Tôi rất vinh dự được phục vụ bạn.",
        ]
        # Check if there are any entities
        if intent == "Thank":
            # If there are entities, perform the necessary actions
            # (you can customize this part based on your use case)
            res = random.choice(thank_responses)
            dispatcher.utter_message(res)
        else:
            # If there are no entities, respond with a default message
            res = "Tôi không hiểu ý định bạn như thế nào."
            dispatcher.utter_message(res)
        
        return []
    
class goodbye(Action):
    def name(self):
        return "goodbye"

    def run(self, dispatcher, tracker, domain):
        # Get entities from the user's input
        intent = tracker.latest_message['intent'].get('name')
        bye_responses = [
            "Tạm biệt bạn!",
            "Tạm biệt bạn! Chúc bạn sức khỏe",
            "bye ",
            "Chào Tạm biệt và chúc bạn thật nhiều sức khỏe."
        ]
        print(intent)
        # Check if there are any entities
        if intent == "goodbye":
            # If there are entities, perform the necessary actions
            # (you can customize this part based on your use case)
            res = random.choice(bye_responses)
            dispatcher.utter_message(res)
        else:
            # If there are no entities, respond with a default message
            res = "Tôi không hiểu ý định bạn như thế nào."
            dispatcher.utter_message(res)
        
        return []



class Support(Action):
    def name(self):
        return "Support"

    def run(self, dispatcher, tracker, domain):
        # Get entities from the user's input
        intent = tracker.latest_message['intent'].get('name')

        # List of possible responses
        support_responses = [
            "Tôi có thể giúp bạn có thể giúp biết về thông tin bác sĩ và đặt lịch khám của phòng khám.",
            "Chúng tôi cung cấp thông tin về bác sĩ và lịch khám, bạn có thể tham khảo.",
            "Nếu bạn cần biết về bác sĩ hoặc đặt lịch khám, tôi ở đây để hỗ trợ."
        ]

        # Check if there are any entities
        if intent == "suppot":
            # If there are entities, choose a random response
            res = random.choice(support_responses)
        else:
            # If there are no entities, respond with a default message
            res = "Tôi không hiểu ý định bạn như thế nào."

        dispatcher.utter_message(res)

        return []


class ActionListDoctors(Action):
    def name(self) -> Text:
        return "ActionListDoctors"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Thực hiện các truy vấn hoặc xử lý để có danh sách bác sĩ
        
        response = requests.get(f'http://localhost:3000/api/get-bacsi')
        response.raise_for_status()
        
        doctors_list = response.json()
        buttons = []
        for doctor in doctors_list:
            buttons.append({"title": doctor['tenBS'], "payload": f"{doctor['_id']}}}"})

        dispatcher.utter_button_message("Đây là danh sách tất cả bác sĩ của phòng khám:", buttons)

        return []