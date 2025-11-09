/*
  Warnings:

  - Added the required column `offset` to the `AttackSummary_lr` table without a default value. This is not possible if the table is not empty.
  - Added the required column `offset` to the `AttackSummary_rf` table without a default value. This is not possible if the table is not empty.
  - Added the required column `offset` to the `NetworkEvent_lr` table without a default value. This is not possible if the table is not empty.
  - Added the required column `offset` to the `NetworkEvent_rf` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "AttackSummary_lr" ADD COLUMN     "offset" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "AttackSummary_rf" ADD COLUMN     "offset" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "NetworkEvent_lr" ADD COLUMN     "offset" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "NetworkEvent_rf" ADD COLUMN     "offset" INTEGER NOT NULL;
