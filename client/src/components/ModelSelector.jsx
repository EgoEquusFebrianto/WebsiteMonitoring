import React, { useContext } from "react";
import { DataContext } from "./DataContext";

const models = ["lr", "rf"];
const nameButton = {"lr": "Logistic Regression", "rf": "Random Forest"}

const ModelSelector = () => {
  const { model, handleModelSwitch } = useContext(DataContext);

  return (
    <div className="flex items-center justify-between bg-white rounded-2xl p-4 shadow-md mb-4 ">
      <h2 className="text-lg font-semibold">Select Model</h2>
      <div className="flex flex-col gap-4">
        {models.map((m) => (
          <button
            key={m}
            onClick={() => {
              handleModelSwitch(m);
            }}
            className={`px-4 py-2 rounded-xl font-medium transition ${
              model === m
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            {nameButton[m].toUpperCase()}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ModelSelector;
