import { useEffect } from "react";

import client from "../api/client";
import { useIdentityStore } from "../state/useIdentityStore";

const CardPreview = () => {
  const records = useIdentityStore((s) => s.records);
  const setRecords = useIdentityStore((s) => s.setRecords);

  useEffect(() => {
    const fetchRecords = async () => {
      const { data } = await client.get("/identities");
      setRecords(data);
    };
    fetchRecords();
  }, [setRecords]);

  return (
    <div className="glass-panel p-6 border border-white/10">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-offWhite">Recent smart IDs</h3>
        <p className="text-xs text-white/60">Identity that protects itself.</p>
      </div>
      <div className="grid md:grid-cols-3 gap-4">
        {records.slice(0, 3).map((record) => (
          <div key={record.id} className="p-4 bg-white/3 rounded-2xl border border-white/10">
            <p className="text-sm text-white/70">{record.external_id}</p>
            <p className="text-lg font-semibold text-offWhite">
              {record.first_name} {record.last_name}
            </p>
            <p className="text-sm text-neonAqua">{record.role}</p>
            <div className="mt-3 flex gap-3 text-xs text-white/70">
              {record.card_png_path && (
                <a href={record.card_png_path} className="underline" target="_blank" rel="noreferrer">
                  PNG
                </a>
              )}
              {record.card_pdf_path && (
                <a href={record.card_pdf_path} className="underline" target="_blank" rel="noreferrer">
                  PDF
                </a>
              )}
              {record.wallet_card_path && (
                <a href={record.wallet_card_path} className="underline" target="_blank" rel="noreferrer">
                  Wallet
                </a>
              )}
            </div>
          </div>
        ))}
        {!records.length && <p className="text-white/60 text-sm">Generate a card to preview assets.</p>}
      </div>
    </div>
  );
};

export default CardPreview;

