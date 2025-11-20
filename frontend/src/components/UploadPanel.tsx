import { useState } from "react";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";

import client from "../api/client";
import { useIdentityStore } from "../state/useIdentityStore";

interface FormFields {
  external_id: string;
  first_name: string;
  last_name: string;
  email?: string;
  role?: string;
  department?: string;
  institution_id: number;
  photo: FileList;
}

const UploadPanel = () => {
  const { register, handleSubmit, reset } = useForm<FormFields>({
    defaultValues: {
      role: "Student",
      department: "Innovation",
      institution_id: 1
    }
  });
  const addRecord = useIdentityStore((s) => s.addRecord);
  const [loading, setLoading] = useState(false);

  const onSubmit = async (data: FormFields) => {
    if (!data.photo?.length) {
      toast.error("Please attach a portrait.");
      return;
    }
    setLoading(true);
    const form = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (key === "photo") return;
      form.append(key, String(value));
    });
    form.append("photo", data.photo[0]);
    try {
      const response = await client.post("/identities", form, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      addRecord(response.data);
      toast.success("Identity generated");
      reset();
    } catch (error) {
      console.error(error);
      toast.error("Generation failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel p-6 border border-white/10">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-semibold text-offWhite">Generate one identity</h3>
          <p className="text-white/70 text-sm">AI crops face, learns your brand and outputs print + wallet cards.</p>
        </div>
        <span className="text-neonAqua text-xs uppercase tracking-[0.4em]">Identify · Verify · Simplify</span>
      </div>
      <form onSubmit={handleSubmit(onSubmit)} className="grid md:grid-cols-2 gap-4">
        <input className="input" placeholder="External ID" {...register("external_id", { required: true })} />
        <input className="input" placeholder="First name" {...register("first_name", { required: true })} />
        <input className="input" placeholder="Last name" {...register("last_name", { required: true })} />
        <input className="input" placeholder="Email" {...register("email")} />
        <input className="input" placeholder="Role" {...register("role")} />
        <input className="input" placeholder="Department" {...register("department")} />
        <input
          className="input"
          type="number"
          placeholder="Institution ID"
          {...register("institution_id", { valueAsNumber: true })}
        />
        <label className="input flex items-center gap-3 cursor-pointer bg-white/5 border-dashed border-white/20">
          <span className="text-white/70 text-sm">Portrait (PNG/JPG)</span>
          <input type="file" accept="image/*" className="hidden" {...register("photo")} />
        </label>
        <div className="md:col-span-2 flex gap-4 items-center">
          <button
            type="submit"
            className="px-6 py-3 rounded-full bg-gradient-to-r from-neonBlue to-neonPurple text-white font-semibold shadow-glow disabled:opacity-50"
            disabled={loading}
          >
            {loading ? "Generating..." : "Create Smart ID"}
          </button>
          <p className="text-sm text-white/60">Outputs PNG · PDF · Digital wallet + QR/NFC token</p>
        </div>
      </form>
    </div>
  );
};

export default UploadPanel;

