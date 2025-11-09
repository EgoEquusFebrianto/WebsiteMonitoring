import express from "express";
import cors from "cors";
import streamRouter from "./src/routes/stream.js";

const app = express();
app.use(cors());
app.use(express.json());

app.use("/api/realtime", streamRouter);

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`🚀 Server Reader running on http://localhost:${PORT}`);
});