import React, { createContext, useState, useEffect } from "react";

export const DataContext = createContext();

export const DataProvider = ({ children }) => {
  const [model, setModel] = useState("rf");
  const [data, setData] = useState({
    networkEvents: [],
    attackSummary: [],
  });

  const startModelStreaming = async (selectedModel) => {
    try {
      const response = await fetch(`http://localhost:5001/start?model=${selectedModel}`);
      if (!response.ok) {
        console.warn("⚠️ Model sudah berjalan atau error:", await response.text());
      } else {
        console.log(`✅ Streaming ${selectedModel.toUpperCase()} dimulai.`);
      }
    } catch (error) {
      console.error("❌ Gagal memulai stream di server-writer:", error);
    }
  };

  // Fungsi untuk menghentikan streaming model sebelumnya
  const stopModelStreaming = async (selectedModel) => {
    try {
      const response = await fetch(`http://localhost:5001/stop?model=${selectedModel}`);
      console.log(await response.text());
    } catch (error) {
      console.error("❌ Gagal menghentikan stream:", error);
    }
  };

  // Ganti model (dari SwitchModelButton)
  const handleModelSwitch = async (newModel) => {
    if (newModel === model) return;

    // Hentikan model lama
    await stopModelStreaming(model);

    // Hapus data lama (tabel LR misalnya)
    await fetch(`http://localhost:4000/api/realtime/clear?model=${model}`, {
      method: "DELETE",
    });
    setModel(newModel);

    // // Mulai streaming model baru
    // await startModelStreaming(newModel);
  };

  useEffect(() => {
    startModelStreaming(model);

    console.log(`🔄 Membuat SSE connection dengan model: ${model}`);
    const eventSource = new EventSource(`http://localhost:4000/api/realtime/stream?model=${model}`);

    eventSource.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);

        setData((prev) => ({
          networkEvents: [
            ...prev.networkEvents.slice(-20), // ambil 20 data lama
            ...(parsed.networkEvents || []),  // tambah 10 data baru
          ],
          attackSummary: parsed.attackSummary || [],
        }));
      } catch (err) {
        console.error("❌ Error parsing SSE data:", err);
      }
    };

    eventSource.onerror = (err) => {
      console.warn("⚠️ SSE error:", err);
      eventSource.close();
    };

    return () => {
      console.log("🧹 Menutup SSE connection sebelumnya");
      eventSource.close();
    };
  }, [model]);

  useEffect(() => {
    console.log("Data terbaru diterima:", data);
  }, [data]);

  return (
    <DataContext.Provider value={{ model, setModel, data, handleModelSwitch }}>
      {children}
    </DataContext.Provider>
  );
};
