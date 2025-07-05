import streamlit as st
import pickle
import pandas as pd
import os
from PIL import Image

# Set page config (should be first Streamlit command)
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load assets
def load_assets():
    """Load model and image assets with error handling"""
    assets = {
        "model": None,
        "image": None
    }
    
    try:
        # Load model
        model_path = os.path.join(BASE_DIR, "pipe.pkl")
        with open(model_path, "rb") as f:
            assets["model"] = pickle.load(f)
            
        # Load image
        image_path = os.path.join(BASE_DIR, "carimage.jpg")
        assets["image"] = Image.open(image_path)
            
    except Exception as e:
        st.error(f"Error loading assets: {e}")
        
    return assets

assets = load_assets()

if assets["model"] is None:
    st.stop()

# App styling
def apply_custom_styles():
    """Apply custom CSS styles"""
    st.markdown("""
    <style>
        /* Main content */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #2c3e50;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #2c3e50;
            color: white;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #3498db;
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            transition: all 0.3s;
            border: none;
            font-weight: bold;
        }
        
        .stButton>button:hover {
            background-color: #2980b9;
            transform: scale(1.05);
        }
        
        /* Input fields */
        .stNumberInput, .stSelectbox {
            margin-bottom: 1rem;
        }
        
        /* Success message */
        .stAlert {
            border-radius: 10px;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main {
                padding: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

apply_custom_styles()

# Car data dictionary (same as original)
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

# App layout
def main():
    """Main app layout and functionality"""
    
    # Sidebar
    with st.sidebar:
        if assets["image"]:
            st.image(assets["image"], use_column_width=True)
        
        st.title("🚗 Car Price Predictor")
        st.markdown("""
        **Welcome to the Car Price Prediction App!**
        
        This app helps you estimate the market value of used cars based on their specifications.
        
        ### Instructions:
        1. Select the car company
        2. Choose the model
        3. Enter purchase year (1995-2019)
        4. Input kilometers driven
        5. Select fuel type
        6. Click **Predict Price**
        
        ### Note:
        - Year range: 1995 to 2019
        - Kilometers: 0 to any reasonable value
        """)
    
    # Main content
    st.title("Car Price Prediction")
    st.markdown("Fill in the details below to get an estimated price for your car.")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Company selection
        company = st.selectbox(
            "Car Company", 
            options=list(car_data.keys()), 
            index=0,
            help="Select the manufacturer of the car"
        )
        
        # Model selection (dynamic based on company)
        models = car_data.get(company, [])
        car_model = st.selectbox(
            "Car Model", 
            options=models, 
            index=0,
            help="Select the specific model of the car"
        )
        
        # Year input with slider
        year = st.slider(
            "Year of Purchase", 
            min_value=1995, 
            max_value=2019, 
            value=2010,
            help="Select the year when the car was first purchased"
        )
    
    with col2:
        # Kilometers driven
        kms_driven = st.number_input(
            "Kilometers Driven", 
            min_value=0, 
            value=50000,
            step=1000,
            help="Enter the total kilometers the car has been driven"
        )
        
        # Fuel type
        fuel_type = st.selectbox(
            "Fuel Type", 
            ["Petrol", "Diesel", "LPG"],
            index=0,
            help="Select the type of fuel the car uses"
        )
        
        # Prediction button
        predict_btn = st.button(
            "🚀 Predict Price", 
            type="primary",
            help="Click to get the estimated price"
        )
    
    # Prediction logic
    if predict_btn:
        with st.spinner("Calculating estimated price..."):
            try:
                # Create input DataFrame
                input_data = pd.DataFrame(
                    [[car_model, company, year, kms_driven, fuel_type]], 
                    columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']
                )
                
                # Make prediction
                prediction = assets["model"].predict(input_data)
                
                # Display result with nice formatting
                st.success(f"""
                ### Estimated Price:  
                **₹{prediction[0]:,.2f}**
                
                *Based on the provided details:
                - Model: {car_model}
                - Year: {year}
                - Kilometers: {kms_driven:,} km
                - Fuel: {fuel_type}*
                """)
                
            except Exception as e:
                st.error(f"""
                ❌ Error in prediction:  
                {str(e)}
                
                Please check your inputs and try again.
                """)

if __name__ == "__main__":
    main()