// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyClYmEG5HSVXDYyvqE2LuHPuT9SHgovkE4",
  authDomain: "proving-groundz.firebaseapp.com",
  databaseURL: "https://proving-groundz-default-rtdb.firebaseio.com",
  projectId: "proving-groundz",
  storageBucket: "proving-groundz.appspot.com",
  messagingSenderId: "660872992357",
  appId: "1:660872992357:web:a844dd5f10bd6a79be188c",
  measurementId: "G-SMZLLLEFHR"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);