import Header from './components/Header';
import Scraper from './components/Scraper';
import QnA from './components/QnA';

function App() {
  return (
    <div className="bg-gray-100 min-h-screen font-sans">
      <Header />
      <main className="container mx-auto p-4">
        <Scraper />
        <QnA />
      </main>
    </div>
  );
}

export default App;
