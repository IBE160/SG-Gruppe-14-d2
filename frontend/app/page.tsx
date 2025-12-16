import { EnvVarWarning } from "@/components/env-var-warning";
import { AuthButton } from "@/components/auth-button";
import { hasEnvVars } from "@/lib/utils";
import { Suspense } from "react";
import { RedirectIfAuthenticated } from "@/components/redirect-if-authenticated";

export default function Home() {

  return (
    <>
      <RedirectIfAuthenticated />
      <main className="min-h-screen flex flex-col items-center bg-gradient-to-b from-blue-50 to-white">
      <div className="flex-1 w-full flex flex-col items-center">
        <nav className="w-full flex justify-center border-b border-b-gray-200 h-16 bg-white">
          <div className="w-full max-w-5xl flex justify-between items-center p-3 px-5 text-sm">
            <div className="flex gap-4 items-center">
              <h1 className="text-xl font-bold text-blue-600">PM Simulator</h1>
            </div>
            {!hasEnvVars ? (
              <EnvVarWarning />
            ) : (
              <Suspense>
                <AuthButton />
              </Suspense>
            )}
          </div>
        </nav>
        <div className="flex-1 flex flex-col max-w-4xl items-center justify-center p-8 text-center">
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            PM Simulator
          </h2>
          <p className="text-xl text-gray-700 mb-4">
            Boligutbyggingsprosjekt Fjordvik
          </p>
          <p className="text-lg text-gray-600 max-w-2xl mb-8">
            Lær prosjektledelse gjennom realistisk forhandling med AI-agenter.
            Naviger budsjettutfordringer, leverandørforhandlinger og kommunale krav
            i et komplekst byggeprosjekt.
          </p>

          <div className="bg-white rounded-lg border-2 border-blue-200 p-8 max-w-2xl mb-8">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Læringsmål</h3>
            <ul className="text-left space-y-2 text-gray-700">
              <li>✓ Forhandlingsteknikk med leverandører og oppdragsgiver</li>
              <li>✓ Budsjettstyring under press (35 MNOK underskudd)</li>
              <li>✓ Håndtering av ufleksible frister</li>
              <li>✓ Balansering av kostnad, kvalitet og tid</li>
              <li>✓ Strategisk beslutningstaking under usikkerhet</li>
            </ul>
          </div>

          <div className="bg-orange-50 border-2 border-orange-200 rounded-lg p-6 max-w-2xl">
            <p className="text-sm font-semibold text-orange-900">
              UTFORDRING: Starttilbudene overstiger budsjettet med 35 MNOK
            </p>
            <p className="text-sm text-orange-800 mt-2">
              Du må forhandle med 3 leverandører og eventuelt kommunen for å redde prosjektet.
              Fristen 15. mai 2026 kan IKKE forlenges!
            </p>
          </div>
        </div>
      </div>
    </main>
    </>
  );
}
