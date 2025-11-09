-- CreateTable
CREATE TABLE "NetworkEvent_lr" (
    "id" SERIAL NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "src_ip" TEXT NOT NULL,
    "dst_ip" TEXT NOT NULL,
    "protocol" TEXT,
    "packet_count" INTEGER NOT NULL,
    "byte_count" INTEGER NOT NULL,
    "flow_duration" DOUBLE PRECISION NOT NULL,
    "label" TEXT NOT NULL,
    "probability" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "NetworkEvent_lr_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "NetworkEvent_rf" (
    "id" SERIAL NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "src_ip" TEXT NOT NULL,
    "dst_ip" TEXT NOT NULL,
    "protocol" TEXT,
    "packet_count" INTEGER NOT NULL,
    "byte_count" INTEGER NOT NULL,
    "flow_duration" DOUBLE PRECISION NOT NULL,
    "label" TEXT NOT NULL,
    "probability" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "NetworkEvent_rf_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AttackSummary_lr" (
    "id" SERIAL NOT NULL,
    "date" TIMESTAMP(3) NOT NULL,
    "total_flows" INTEGER NOT NULL,
    "benign_count" INTEGER NOT NULL,
    "ddos_count" INTEGER NOT NULL,
    "ddos_ratio" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "AttackSummary_lr_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AttackSummary_rf" (
    "id" SERIAL NOT NULL,
    "date" TIMESTAMP(3) NOT NULL,
    "total_flows" INTEGER NOT NULL,
    "benign_count" INTEGER NOT NULL,
    "ddos_count" INTEGER NOT NULL,
    "ddos_ratio" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "AttackSummary_rf_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SystemPerformance_lr" (
    "id" SERIAL NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "accuracy" DOUBLE PRECISION NOT NULL,
    "precision" DOUBLE PRECISION NOT NULL,
    "recall" DOUBLE PRECISION NOT NULL,
    "f1_score" DOUBLE PRECISION NOT NULL,
    "latency_ms" DOUBLE PRECISION,
    "cpu_usage" DOUBLE PRECISION,
    "memory_usage" DOUBLE PRECISION,

    CONSTRAINT "SystemPerformance_lr_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SystemPerformance_rf" (
    "id" SERIAL NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "accuracy" DOUBLE PRECISION NOT NULL,
    "precision" DOUBLE PRECISION NOT NULL,
    "recall" DOUBLE PRECISION NOT NULL,
    "f1_score" DOUBLE PRECISION NOT NULL,
    "latency_ms" DOUBLE PRECISION,
    "cpu_usage" DOUBLE PRECISION,
    "memory_usage" DOUBLE PRECISION,

    CONSTRAINT "SystemPerformance_rf_pkey" PRIMARY KEY ("id")
);
