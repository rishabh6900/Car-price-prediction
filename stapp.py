import streamlit as st
import pickle
import pandas as pd
from sklearn.pipeline import Pipeline

# Load the trained model
try:
    with open("pipe.pkl", "rb") as pickle_in:
        pipe = pickle.load(pickle_in)
except Exception as e:
    st.error(f"Error loading the model: {e}")
    pipe = None

if pipe is None:
    st.stop()

st.title("Car Price Prediction App 🚗")

# Dictionary mapping companies to their models
car_data = {
   "Hyundai": ['Hyundai Santro Xing', 'Hyundai Grand i10', 'Hyundai Eon', 'Hyundai Elite i20', 'Hyundai i20 Sportz', 'Hyundai i20 Magna', 'Hyundai Verna Transform', 'Hyundai i10 Magna', 'Hyundai Verna Fluidic', 'Hyundai i20 Asta', 'Hyundai Eon Era', 'Hyundai Creta 1.6', 'Hyundai i20 Active', 'Hyundai i10 Sportz', 'Hyundai i10', 'Hyundai Accent GLX', 'Hyundai Elantra SX', 'Hyundai Accent', 'Hyundai Verna', 'Hyundai Xcent Base', 'Hyundai Accent Executive', 'Hyundai Verna 1.4', 'Hyundai Verna 1.6', 'Hyundai Sonata Transform', 'Hyundai Xcent SX', 'Hyundai Santro', 'Hyundai Getz Prime', 'Hyundai Santro AE', 'Hyundai Verna VGT', 'Hyundai i10 Era', 'Hyundai Elantra 1.8', 'Hyundai i20 Select', 'Hyundai Getz GLE', 'Hyundai Creta', 'Hyundai Getz', 'Hyundai Santro Xing'],
    
    "Mahindra": ['Mahindra Jeep CL550', 'Mahindra Scorpio SLE', 'Mahindra Scorpio S10', 'Mahindra Bolero DI', 'Mahindra Scorpio S4', 'Mahindra Scorpio VLX', 'Mahindra Quanto C8', 'Mahindra XUV500 W8', 'Mahindra Bolero SLE', 'Mahindra Thar CRDe', 'Mahindra TUV300 T4', 'Mahindra KUV100 K8', 'Mahindra Scorpio 2.6', 'Mahindra Scorpio W', 'Mahindra Scorpio SLX', 'Mahindra XUV500', 'Mahindra Jeep MM', 'Mahindra Xylo E4', 'Mahindra Bolero Power', 'Mahindra Scorpio Vlx', 'Mahindra Logan Diesel', 'Mahindra XUV500 W10', 'Mahindra TUV300 T8', 'Mahindra XUV500 W6', 'Mahindra Scorpio LX', 'Mahindra KUV100', 'Mahindra Xylo D2', 'Mahindra Xylo E8', 'Mahindra Logan', 'Mahindra Quanto C4'],
    
    "Ford": ['Ford EcoSport Titanium', 'Ford Figo', 'Ford EcoSport Ambiente', 'Ford EcoSport', 'Ford Figo Diesel', 'Ford Figo Duratorq', 'Ford EcoSport Trend', 'Ford Fiesta', 'Ford Fiesta SXi', 'Ford Ikon 1.3', 'Ford Ikon 1.6', 'Ford Figo Petrol', 'Ford Endeavor 4x4', 'Ford Fusion 1.4'],
    
    "Maruti": ['Maruti Suzuki Alto', 'Maruti Suzuki Stingray', 'Maruti Suzuki Vitara', 'Maruti Suzuki Swift', 'Maruti Suzuki Wagon', 'Maruti Suzuki Baleno', 'Maruti Suzuki Dzire', 'Maruti Suzuki SX4', 'Maruti Suzuki Ertiga', 'Maruti Suzuki Ritz', 'Maruti Suzuki Esteem', 'Maruti Suzuki Ciaz', 'Maruti Suzuki Zen', 'Maruti Suzuki Versa', 'Maruti Suzuki Omni', 'Maruti Suzuki 800', 'Maruti Suzuki Estilo', 'Maruti Suzuki Maruti', 'Maruti Suzuki Celerio', 'Maruti Suzuki S'],
    
    "Skoda": ['Skoda Fabia Classic', 'Skoda Yeti Ambition', 'Skoda Fabia 1.2L', 'Skoda Rapid Elegance', 'Skoda Superb 1.8', 'Skoda Laura', 'Skoda Octavia Classic', 'Skoda Fabia'],
    
    "Audi": ['Audi A8', 'Audi Q7', 'Audi A4 1.8', 'Audi A4 2.0', 'Audi Q3 2.0', 'Audi A6 2.0', 'Audi Q5 2.0', 'Audi A3 Cabriolet'],
    
    "Toyota": ['Toyota Innova 2.0', 'Toyota Corolla Altis', 'Toyota Etios GD', 'Toyota Etios Liva', 'Toyota Innova 2.5', 'Toyota Corolla H2', 'Toyota Fortuner', 'Toyota Etios', 'Toyota Fortuner 3.0', 'Toyota Qualis', 'Toyota Etios G'],
    
    "Renault": ['Renault Lodgy 85', 'Renault Duster 110', 'Renault Duster 85', 'Renault Kwid', 'Renault Scala RxL', 'Renault Kwid RXT', 'Renault Kwid 1.0', 'Renault Duster 85PS', 'Renault Duster RxL'],
    
    "Honda": ['Honda City 1.5', 'Honda Amaze', 'Honda Amaze 1.5', 'Honda City', 'Honda City ZX', 'Honda City VX', 'Honda City SV', 'Honda Brio', 'Honda Brio V', 'Honda Accord', 'Honda Mobilio', 'Honda Mobilio S', 'Honda Jazz VX', 'Honda Jazz S', 'Honda WR V'],
    
    "Datsun": ['Datsun Redi GO', 'Datsun GO T', 'Datsun Go Plus'],
    
    "Mitsubishi": ['Mitsubishi Pajero Sport', 'Mitsubishi Lancer 1.8'],
    
    "Tata": ['Tata Indigo eCS', 'Tata Indica V2', 'Tata Nano Cx', 'Tata Sumo Victa', 'Tata Indigo CS', 'Tata Zest XE', 'Tata Zest Quadrajet', 'Tata Sumo Gold', 'Tata Manza Aura', 'Tata Manza Aqua', 'Tata Vista Quadrajet', 'Tata Indica eV2', 'Tata Indigo LX', 'Tata Indigo LS', 'Tata Nano GenX', 'Tata Venture EX', 'Tata Bolt XM', 'Tata Sumo Grande', 'Tata Tiago Revotron', 'Tata Tiago Revotorq', 'Tata Indigo Marina', 'Tata Nano LX', 'Tata Manza ELAN'],
    
    "Volkswagen": ['Volkswagen Polo Highline', 'Volkswagen Vento Highline', 'Volkswagen Polo Comfortline', 'Volkswagen Polo', 'Volkswagen Jetta Highline', 'Volkswagen Polo Trendline', 'Volkswagen Polo Highline1.2L', 'Volkswagen Vento Konekt', 'Volkswagen Vento Comfortline', 'Volkswagen Jetta Comfortline', 'Volkswagen Passat Diesel'],
    
    "Chevrolet": ['Chevrolet Spark LS', 'Chevrolet Beat LT', 'Chevrolet Spark', 'Chevrolet Beat', 'Chevrolet Beat LS', 'Chevrolet Sail UVA', 'Chevrolet Beat Diesel', 'Chevrolet Tavera Neo', 'Chevrolet Tavera LS', 'Chevrolet Enjoy 1.4', 'Chevrolet Cruze LTZ', 'Chevrolet Sail 1.2', 'Chevrolet Enjoy'],
    
    "Mini": ['Mini Cooper S'],
    
    "BMW": ['BMW 3 Series', 'BMW 7 Series', 'BMW 5 Series', 'BMW X1 xDrive20d', 'BMW X1 sDrive20d', 'BMW X1'],
    
    "Nissan": ['Nissan Micra XV', 'Nissan Sunny', 'Nissan Terrano XL', 'Nissan X Trail', 'Nissan Micra XL'],
    
    "Hindustan": ['Hindustan Motors Ambassador'],
    
    "Fiat": ['Fiat Punto Emotion', 'Fiat Petra ELX', 'Fiat Linea Emotion'],
    
    "Force": ['Force Motors Force', 'Force Motors One'],
    
    "Mercedes": ['Mercedes Benz GLA', 'Mercedes Benz B', 'Mercedes Benz C', 'Mercedes Benz A'],
    
    "Land": ['Land Rover Freelander'],
    
    "Jaguar": ['Jaguar XE XE', 'Jaguar XF 2.2'],
    
    "Jeep": ['Jeep Wrangler Unlimited'],
    
    "Volvo": ['Volvo S80 Summum']
}

companies = list(car_data.keys())

# User Input
company = st.selectbox("Car Company", options=companies, index=0)
models = car_data.get(company, [])

# Select car model dynamically based on selected company
car_model = st.selectbox("Car Model", options=models, index=0)
# custom_model = st.text_input("Or Enter Custom Car Model", "")

year = st.number_input("Year of Purchase", min_value=1995, max_value=2019, value=2009)
kms_driven = st.number_input("Kilometers Driven", min_value=0, value=50000)
fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "LPG"])


st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #10850d;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 24px;
        transition: 0.3s;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #10850d;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Use custom model if entered
# Predict Button
if st.button("Predict Price 💰"):
    input_data = pd.DataFrame([[car_model, company, year, kms_driven, fuel_type]], 
                              columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])
    
    try:
        prediction = pipe.predict(input_data)
        st.success(f"Estimated Price: ₹{prediction[0]:,.2f}")
    except Exception as e:
        st.error(f"Error in prediction: {e}")

st.sidebar.image("carimage.jpg")
st.sidebar.title(" Welcome Car Price Prediction App")
st.sidebar.text("*Here is Max year 2019 and Min years 1995")
st.sidebar.text("*Here is Max Km 50000 and Min Km 0")
