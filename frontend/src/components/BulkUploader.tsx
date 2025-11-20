import { useState } from "react";
import toast from "react-hot-toast";

import client from "../api/client";

const BulkUploader = () => {
  const [institutionId, setInstitutionId] = useState(1);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    if (!file) {
      toast.error("Attach CSV or Excel file");
      return;
    }
    const form = new FormData();
    form.append("institution_id", String(institutionId));
    form.append("file", file);
    setLoading(true);
    try {
      const { data } = await client.post("/identities/bulk", form, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      toast.success(`Processed ${data.processed} identities`);
    } catch (error) {
      console.error(error);
      toast.error("Bulk upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel p-6 border border-white/10">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-offWhite">Bulk Excel / CSV</h3>
        <p className="text-xs text-white/60">Smart IDs for smarter institutions.</p>
      </div>
      <div className="grid md:grid-cols-3 gap-4">
        <div className="md:col-span-1">
          <label className="text-sm text-white/70">Institution ID</label>
          <input
            type="number"
            value={institutionId}
            onChange={(e) => setInstitutionId(Number(e.target.value))}
            className="input mt-2"
          />
        </div>
        <div className="md:col-span-2">
          <label className="text-sm text-white/70">Data file</label>
          <div className="mt-2 flex items-center gap-3 bg-white/5 border border-white/15 rounded-2xl px-4 py-3">
            <input
              type="file"
              accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="text-sm text-white/70"
            />
            {file && <span className="text-xs text-white/50">{file.name}</span>}
          </div>
        </div>
      </div>
      <div className="mt-6 flex items-center gap-4">
        <button
          onClick={upload}
          disabled={loading}
          className="px-5 py-3 rounded-full bg-gradient-to-r from-neonBlue to-neonPurple text-white font-semibold shadow-glow disabled:opacity-50"
        >
          {loading ? "Uploading..." : "Bulk generate"}
        </button>
        <p className="text-sm text-white/60">Spreadsheet columns: external_id, first_name, last_name, role, department, photo_url</p>
      </div>
    </div>
  );
};

export default BulkUploader;

