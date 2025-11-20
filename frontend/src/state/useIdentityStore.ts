import { create } from "zustand";

export interface IdentityRecord {
  id: number;
  first_name: string;
  last_name: string;
  role?: string;
  department?: string;
  status: string;
  card_png_path?: string;
  card_pdf_path?: string;
  wallet_card_path?: string;
  qr_png_path?: string;
  secure_token?: string;
}

interface IdentityState {
  records: IdentityRecord[];
  setRecords: (records: IdentityRecord[]) => void;
  addRecord: (record: IdentityRecord) => void;
}

export const useIdentityStore = create<IdentityState>((set) => ({
  records: [],
  setRecords: (records) => set({ records }),
  addRecord: (record) => set((state) => ({ records: [record, ...state.records] }))
}));

