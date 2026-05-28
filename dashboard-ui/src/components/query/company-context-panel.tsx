"use client";

import { Building2, FileText, Loader2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import type { CompanyResolveData, IngestionRunSummary } from "@/types/company";

interface CompanyContextPanelProps {
  company: CompanyResolveData | null;
  ingestion?: IngestionRunSummary | null;
  loading?: boolean;
  error?: string | null;
}

export function CompanyContextPanel({
  company,
  ingestion,
  loading,
  error,
}: CompanyContextPanelProps) {
  if (loading) {
    return (
      <div className="flex items-center gap-2 rounded-lg border border-border/60 bg-muted/20 px-3 py-2 text-xs text-muted-foreground">
        <Loader2 className="h-3.5 w-3.5 animate-spin" />
        종목·공시 정보 확인 중…
      </div>
    );
  }

  if (error) {
    return (
      <p className="text-xs text-amber-400/90">{error}</p>
    );
  }

  if (!company) return null;

  const s = company.stats;

  return (
    <div className="w-full space-y-3 rounded-lg border border-primary/20 bg-primary/5 p-3">
      <div className="flex flex-wrap items-start gap-2">
        <Building2 className="mt-0.5 h-4 w-4 text-primary" />
        <div className="min-w-0 flex-1">
          <p className="font-semibold text-foreground">{company.company_name}</p>
          <div className="mt-1 flex flex-wrap gap-1.5">
            <Badge variant="secondary">ticker {company.ticker}</Badge>
            <Badge variant="outline">corp {company.corp_code}</Badge>
            <Badge variant="outline">{company.market}</Badge>
            {company.cache_ready && (
              <Badge className="bg-emerald-600/80">데이터 준비됨</Badge>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs sm:grid-cols-3 md:grid-cols-6">
        <Stat label="뉴스" value={s.news_count} />
        <Stat label="공시" value={s.disclosure_count} />
        <Stat label="주가" value={s.price_count} />
        <Stat label="chunk" value={s.chunk_count} />
        <Stat label="embedding" value={s.embedding_count} />
        <Stat label="미임베딩" value={s.pending_embedding_count} />
      </div>

      {ingestion && (
        <p className="text-xs text-muted-foreground">
          수집: 문서 {ingestion.documents}건 · chunk {ingestion.chunks} ·
          신규 embedding {ingestion.embeddings_created} ·
          기존 재사용 {ingestion.embeddings_skipped}
          {ingestion.skipped_collectors.length > 0 && (
            <span className="ml-1 text-emerald-400/90">
              (스킵: {ingestion.skipped_collectors.join(", ")})
            </span>
          )}
        </p>
      )}

      {company.recent_disclosures.length > 0 && (
        <div>
          <p className="mb-1.5 flex items-center gap-1 text-xs font-medium text-muted-foreground">
            <FileText className="h-3.5 w-3.5" />
            최근 공시
          </p>
          <ul className="max-h-32 space-y-1 overflow-y-auto text-xs">
            {company.recent_disclosures.map((d) => (
              <li
                key={`${d.receipt_no}-${d.report_name}`}
                className="rounded border border-border/40 bg-card/40 px-2 py-1"
              >
                <span className="text-muted-foreground">
                  {d.receipt_date || "—"}
                </span>
                <span className="ml-2 text-foreground">{d.report_name}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded border border-border/40 bg-card/30 px-2 py-1.5 text-center">
      <p className="text-[10px] text-muted-foreground">{label}</p>
      <p className="font-mono font-semibold">{value}</p>
    </div>
  );
}
