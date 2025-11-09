import express from "express";
import { getLatestNetworkEvents } from "../services/networkService.js";
import { getLatestAttackSummary } from "../services/attackService.js";
import prisma from "../prisma/client.js";

const router = express.Router();
var offsets_def = 0;

// Endpoint SSE
router.get("/stream", async (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  res.flushHeaders();

  console.log("👀 Client connected to stream");

  const sendData = async () => {
    try {
      console.log("Offset Before:", offsets_def);
      const model = req.query.model || "lr";
      const [networkEvents, attackSummary] = await Promise.all([
        getLatestNetworkEvents(model, offsets_def, 10),
        getLatestAttackSummary(model, offsets_def, 1),
      ]);

      // Hanya kirim dan naikkan offset jika data baru ditemukan
      if ((networkEvents && networkEvents.length > 0) || (attackSummary && attackSummary.length > 0)) {
        const payload = {
          timestamp: new Date(),
          networkEvents,
          attackSummary,
        };
        res.write(`data: ${JSON.stringify(payload)}\n\n`);
        offsets_def++; // hanya increment jika data valid
        console.log("✅ Data dikirim. Offset sekarang:", offsets_def);
      } else {
        console.log("⚠️ Tidak ada data baru, offset tidak berubah:", offsets_def);
      }
    } catch (err) {
      console.error("❌ Error streaming data:", err);
    }
  };

  // Kirim data pertama kali langsung
  await sendData();

  // Kirim data tiap 3 detik (sesuai interval server-writer)
  const interval = setInterval(sendData, 3000);

  // Handle koneksi terputus
  req.on("close", () => {
    console.log("❌ Client disconnected from stream");
    clearInterval(interval);
  });
});

router.delete("/clear", async (req, res) => {
  const model = (req.query.model || "").toLowerCase();
  if (!["lr", "rf"].includes(model)) {
    return res.status(400).json({ error: "Model tidak valid. Gunakan 'lr' atau 'rf'." });
  }

  const networkTable = `NetworkEvent_${ model }`;
  const attackTable  = `AttackSummary_${ model }`;

  try {
    await prisma.$transaction([
      prisma[networkTable].deleteMany({}),
      prisma[attackTable].deleteMany({})
    ]);

    offsets_def = 0

    return res.json({ success: true, message: `Tabel ${networkTable} & ${attackTable} telah dibersihkan.` });
  } catch (err) {
    console.error("❌ Error clearing tables:", err);
    return res.status(500).json({ success: false, message: "Internal server error" });
  }
});

export default router;
