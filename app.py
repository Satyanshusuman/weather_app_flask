from flask import Flask,render_template,request
import requests
from datetime import datetime
app=Flask(__name__)
headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

class Forecast:
    def forecast_img(res):
        img=[]
        for i in range(1,9):
            data=res["forecast"]["forecastday"][i]["day"]["condition"]["icon"]
            img.append(data)
        return img
    def forecast_day(res):
        days=[]
        for i in range(1,9):
           data=datetime.strptime(res["forecast"]["forecastday"][i]["date"],"%Y-%m-%d").strftime("%a")      
           days.append(data)
        return days
    def forecast_temp(res):
        temps=[]
        for i in range(1,9):
            data=res["forecast"]["forecastday"][2]["day"]["avgtemp_c"]
            temps.append(data)
        return temps


@app.route("/",methods=["GET"])
def home():
    url="https://api.weatherapi.com/v1/forecast.json?key=bd3ef40472f44e2398795707231805&q=patna&days=9"
    res=requests.get(url,headers=headers).json()
    img=Forecast.forecast_img(res)
    days=Forecast.forecast_day(res)
    temps=Forecast.forecast_temp(res)

    data= { "place_name":res["location"]["name"],
            "temp":res["current"]["temp_c"],
            "day":datetime.now().strftime("%d %B %Y %A"),
            "weather_description":res["current"]["condition"]["text"],
            "precip":res["current"]["precip_mm"],
            "humidity":res["current"]["humidity"], 
            "wind_speed":res["current"]["wind_kph"],
        }
    return render_template ("weather.html",data=data,days=days,temps=temps,img=img)

@app.route("/current",methods=["POST"])
def weather():
    if request.method=="POST" :
        city=request.form["city_name"]
        url=f"https://api.weatherapi.com/v1/forecast.json?key=bd3ef40472f44e2398795707231805&q={city}&days=9"
        res=requests.get(url,headers=headers).json()
    img=Forecast.forecast_img(res)
    days=Forecast.forecast_day(res)
    temps=Forecast.forecast_temp(res)  
    data= { "place_name":res["location"]["name"],
            "temp":res["current"]["temp_c"],
            "day":res["location"]["localtime"],
            "weather_description":datetime.now().strftime("%d %B %Y %A"),
            "precip":res["current"]["precip_mm"],
            "humidity":res["current"]["humidity"], 
            "wind_speed":res["current"]["wind_kph"],
          }
    return render_template ("weather.html",data=data,days=days,temps=temps,img=img)


if __name__=="__main__":
    app.run(debug=True)