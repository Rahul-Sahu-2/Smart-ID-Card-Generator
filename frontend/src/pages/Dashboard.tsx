import Hero from "../components/Hero";
import StatsGrid from "../components/StatsGrid";
import UploadPanel from "../components/UploadPanel";
import BulkUploader from "../components/BulkUploader";
import CardPreview from "../components/CardPreview";
import VerificationFeed from "../components/VerificationFeed";
import PosterBrief from "../components/PosterBrief";

const Dashboard = () => {
  return (
    <>
      <Hero />
      <StatsGrid />
      <section className="px-6 py-12">
        <div className="max-w-6xl mx-auto grid lg:grid-cols-[1.1fr,0.9fr] gap-8">
          <UploadPanel />
          <VerificationFeed />
        </div>
        <div className="max-w-6xl mx-auto mt-8 grid lg:grid-cols-[1.2fr,0.8fr] gap-8">
          <CardPreview />
          <PosterBrief />
        </div>
        <div className="max-w-6xl mx-auto mt-8">
          <BulkUploader />
        </div>
      </section>
    </>
  );
};

export default Dashboard;

