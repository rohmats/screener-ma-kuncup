// API Route: Get list of BEI stocks
// GET /api/stocks

import { NextResponse } from 'next/server';

export const runtime = 'edge';

// Common BEI stocks (top 100 by market cap and liquidity)
const BEI_STOCKS = [
  'BBCA', 'BBRI', 'BMRI', 'TLKM', 'ASII', 'UNVR', 'HMSP', 'ICBP', 'INDF', 'KLBF',
  'SMGR', 'UNTR', 'GGRM', 'EXCL', 'INTP', 'PTBA', 'ADRO', 'ITMG', 'AKRA', 'BBTN',
  'PGAS', 'LPKR', 'SMRA', 'SCMA', 'MIDI', 'ERAA', 'MAPI', 'BRPT', 'TKIM', 'CPIN',
  'JPFA', 'TBIG', 'BSDE', 'PWON', 'CTRA', 'EMTK', 'JSMR', 'WIKA', 'WSKT', 'PTPP',
  'ANTM', 'TINS', 'INCO', 'SMBR', 'WTON', 'MEDC', 'ELSA', 'BYAN', 'ESSA', 'HRUM',
  'DOID', 'KKGI', 'ACES', 'MNCN', 'TOWR', 'KIJA', 'DMAS', 'BEST', 'BUKA', 'GOTO',
  'AMRT', 'ACES', 'BRIS', 'BTPS', 'BJBR', 'BBNI', 'SDRA', 'TARA', 'BFIN', 'PNBN',
  'MEGA', 'BBKP', 'NISP', 'BNLI', 'BCAP', 'BNGA', 'BBHI', 'PNBS', 'BJTM', 'DNAR',
  'AALI', 'LSIP', 'SIMP', 'TBLA', 'TAPG', 'SRIL', 'SGRO', 'DSNG', 'BWPT', 'PALM',
  'AGRO', 'UNSP', 'BTEK', 'MPPA', 'SMAR', 'ANJT', 'MYOR', 'ULTJ', 'ROTI', 'MLBI',
];

export async function GET() {
  return NextResponse.json({
    stocks: BEI_STOCKS,
    total: BEI_STOCKS.length,
    source: 'BEI (Indonesia Stock Exchange)',
  });
}
