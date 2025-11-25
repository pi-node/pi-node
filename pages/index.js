import { useState } from "react";
import { configureStore, createSlice } from "@reduxjs/toolkit";
import { Provider, useDispatch, useSelector } from "react-redux";
import { motion } from "framer-motion";
import useSWR from "swr";
import axios from "axios";

// Redux Toolkit: Tema (Dark Mode)
const themeSlice = createSlice({
  name: "theme",
  initialState: { darkMode: false },
  reducers: {
    toggleDarkMode: (state) => {
      state.darkMode = !state.darkMode;
    },
  },
});

const store = configureStore({ reducer: { theme: themeSlice.reducer } });

// API Fetcher
const fetcher = (url) => axios.get(url).then((res) => res.data);

function Navbar() {
  const dispatch = useDispatch();
  const darkMode = useSelector((state) => state.theme.darkMode);

  return (
    <nav className={`p-4 flex justify-between ${darkMode ? "bg-gray-900" : "bg-white"} shadow-md`}>
      <h1 className="text-lg font-bold text-blue-600 dark:text-white">Simpul Pi</h1>
      <button 
        className="px-4 py-2 rounded bg-blue-500 text-white" 
        onClick={() => dispatch(themeSlice.actions.toggleDarkMode())}>
        {darkMode ? "Light Mode" : "Dark Mode"}
      </button>
    </nav>
  );
}

function Home() {
  const darkMode = useSelector((state) => state.theme.darkMode);
  const { data, error } = useSWR("/api/data", fetcher);

  if (error) return <p className="text-red-500">Error loading data</p>;
  if (!data) return <p>Loading...</p>;

  return (
    <div className={`min-h-screen ${darkMode ? "bg-gray-800 text-white" : "bg-gray-100 text-black"}`}>
      <Navbar />
      <div className="max-w-4xl mx-auto p-6">
        <motion.h1 
          className="text-3xl font-bold" 
          initial={{ opacity: 0, y: -20 }} 
          animate={{ opacity: 1, y: 0 }} 
          transition={{ duration: 0.5 }}>
          Selamat Datang di Simpul Pi
        </motion.h1>
        <motion.p 
          className="mt-4" 
          initial={{ opacity: 0 }} 
          animate={{ opacity: 1 }} 
          transition={{ delay: 0.5 }}>
          Platform inovatif untuk ekosistem Pi Network.
        </motion.p>
        <div className="mt-6">
          <h2 className="text-xl font-semibold">Data API:</h2>
          <pre className="bg-gray-200 dark:bg-gray-700 p-4 rounded">{JSON.stringify(data, null, 2)}</pre>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Provider store={store}>
      <Home />
    </Provider>
  );
}
