"use client";

import { useState } from "react";
import { Loader2, Play, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CompanySearchInput } from "@/components/company-selector/CompanySearchInput";
import { CompanyDropdown } from "@/components/company-selector/CompanyDropdown";
import { TopicKeywordInput } from "@/components/company-selector/TopicKeywordInput";
import { SelectedCompanyCard } from "@/components/company-selector/SelectedCompanyCard";
import { useCompanySearch } from "@/hooks/use-company-search";
import { useSelectedTicker } from "@/hooks/use-selected-ticker";
import type { CompanyResolveData } from "@/types/company";
import type { LoadStatus } from "@/types/dashboard";

interface QueryExecutionPanelProps {
  status: LoadStatus;
  engineRunning: boolean;
  traceId: string | null;
  displayQuery?: string;
  selectedTicker: string | null;
  onRunQuery: (payload: {
    ticker: string;
    company: string;
    keywords: string[];
  }) => void;
  onLoadByTraceId: (traceId: string) => void;
  companyContext?: CompanyResolveData | null;
}

export function QueryExecutionPanel({
  status,
  engineRunning,
  traceId,
  displayQuery,
  selectedTicker: externalTicker,
  onRunQuery,
  onLoadByTraceId,
  companyContext,
}: QueryExecutionPanelProps) {
  const [searchText, setSearchText] = useState("");
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [traceInput, setTraceInput] = useState("");

  const {
    selectedCompany,
    selectedTicker,
    keywords,
    setKeywords,
    selectCompany,
    clearSelection,
    parseKeywords,
  } = useSelectedTicker();

  const searchEnabled = !selectedCompany && searchText.trim().length > 0;
  const { results, loading: searchLoading, error: searchError } = useCompanySearch(
    searchText,
    searchEnabled,
  );
  const showDropdown =
    dropdownOpen && !selectedCompany && searchText.trim().length > 0;

  const busy = status === "loading" || engineRunning;
  const ticker = selectedCompany?.ticker ?? externalTicker;
  const kwList = parseKeywords();

  const handleSelect = (item: (typeof results)[0]) => {
    selectCompany(item);
    setSearchText(item.company_name);
    setDropdownOpen(false);
  };

  const handleRun = () => {
    if (!selectedCompany) return;
    onRunQuery({
      ticker: selectedCompany.ticker,
      company: selectedCompany.company_name,
      keywords: kwList,
    });
  };

  return (
    <Card className="overflow-visible border-primary/30 bg-card">
      <CardHeader>
        <CardTitle>종목 선택 · 토픽 분석</CardTitle>
        <p className="text-xs text-muted-foreground">
          종목은 자동완성에서 <strong>직접 선택</strong>하고, 분석 키워드는 별도로
          입력합니다. 부분 문자열 자동 확정은 사용하지 않습니다.
        </p>
      </CardHeader>
      <CardContent className="flex flex-col gap-4 overflow-visible">
        <CompanySearchInput
          value={searchText}
          onChange={(v) => {
            setSearchText(v);
            setDropdownOpen(true);
            if (selectedCompany && v !== selectedCompany.company_name) {
              clearSelection();
            }
          }}
          onFocus={() => setDropdownOpen(true)}
          disabled={busy}
          dropdown={
            <CompanyDropdown
              items={results}
              loading={searchLoading}
              error={searchError}
              visible={showDropdown}
              onSelect={handleSelect}
            />
          }
        />

        <SelectedCompanyCard
          company={selectedCompany}
          keywords={kwList}
          onClear={() => {
            clearSelection();
            setSearchText("");
            setDropdownOpen(false);
          }}
        />

        <TopicKeywordInput
          value={keywords}
          onChange={setKeywords}
          disabled={busy}
        />

        <div className="flex flex-wrap items-end gap-2">
          <Button
            type="button"
            disabled={busy || !selectedCompany}
            onClick={handleRun}
          >
            {engineRunning ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Search className="h-4 w-4" />
            )}
            {engineRunning ? "분석 중…" : "분석 실행"}
          </Button>

          <div className="flex flex-wrap items-end gap-2 sm:ml-auto">
            <div className="min-w-[160px] space-y-1">
              <label className="text-xs text-muted-foreground">trace_id</label>
              <Input
                value={traceInput}
                onChange={(e) => setTraceInput(e.target.value)}
                placeholder={traceId ?? ""}
                disabled={busy}
              />
            </div>
            <Button
              type="button"
              variant="outline"
              size="sm"
              disabled={busy || !traceInput.trim()}
              onClick={() => onLoadByTraceId(traceInput.trim())}
            >
              <Play className="h-4 w-4" />
              Load
            </Button>
          </div>
        </div>

        {companyContext && ticker && (
          <p className="text-xs text-muted-foreground">
            DB: {companyContext.company_name} ({companyContext.ticker}) · embeddings{" "}
            {companyContext.stats.embedding_count}
          </p>
        )}

        {displayQuery && (
          <p className="text-xs text-muted-foreground">
            Runtime query:{" "}
            <span className="font-medium text-foreground">{displayQuery}</span>
            {traceId && (
              <span className="ml-2 font-mono opacity-60">({traceId})</span>
            )}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
