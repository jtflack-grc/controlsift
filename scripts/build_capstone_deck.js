const pptxgen = require('pptxgenjs');
const path = require('path');

async function main() {
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5
pptx.author = 'John Flack';
pptx.subject = 'ControlSift capstone presentation';
pptx.title = 'ControlSift — Can a small language model tell proof from paperwork?';
pptx.company = 'Independent applied research';
pptx.lang = 'en-US';
pptx.theme = {
  headFontFace: 'Aptos Display',
  bodyFontFace: 'Aptos',
  lang: 'en-US'
};
pptx.defineSlideMaster({
  title: 'MASTER',
  background: { color: '07100C' },
  objects: [
    { rect: { x:0, y:0, w:13.333, h:0.07, fill:{color:'7FFFB2'}, line:{color:'7FFFB2'} } },
    { text: { text:'CONTROLSIFT / AI ASSURANCE RESEARCH', options:{ x:0.55, y:0.18, w:5.4, h:0.28, fontFace:'Consolas', fontSize:9, color:'7FFFB2', bold:true, margin:0, charSpacing:1.2 } } },
    { text: { text:'John Flack', options:{ x:10.8, y:0.18, w:1.95, h:0.28, fontFace:'Aptos', fontSize:9, color:'97AEA1', align:'right', margin:0 } } },
    { line: { x:0.55, y:7.16, w:12.23, h:0, line:{color:'263A31', width:1} } },
    { text: { text:'Synthetic research artifact • human judgment remains authoritative', options:{ x:0.55, y:7.2, w:7.1, h:0.2, fontFace:'Aptos', fontSize:7.8, color:'769083', margin:0 } } },
  ],
  slideNumber: { x:12.42, y:7.19, w:0.35, h:0.18, fontFace:'Consolas', fontSize:8, color:'769083', align:'right', margin:0 }
});

const C = {
  bg:'07100C', panel:'0D1913', panel2:'122019', line:'294037', green:'7FFFB2', green2:'38E881', fg:'F4FBF6', muted:'AAC0B2', dim:'789083', amber:'F4C66A', red:'FF8B8B', blue:'8EC7FF', white:'FFFFFF'
};

function addTitle(slide, kicker, title, subtitle='') {
  slide.addText(kicker.toUpperCase(), {x:0.58,y:0.62,w:5.2,h:0.24,fontFace:'Consolas',fontSize:10,bold:true,color:C.green2,charSpacing:1.3,margin:0});
  slide.addText(title, {x:0.58,y:0.88,w:12.1,h:0.65,fontFace:'Aptos Display',fontSize:28,bold:true,color:C.fg,margin:0,fit:'shrink'});
  if (subtitle) slide.addText(subtitle, {x:0.6,y:1.53,w:11.7,h:0.42,fontFace:'Aptos',fontSize:13.5,color:C.muted,margin:0,fit:'shrink'});
}
function addPill(slide, x,y,w,text,fill=C.panel2,color=C.green,line=C.line) {
  slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h:0.34,rectRadius:0.06,fill:{color:fill},line:{color:line,width:1},radius:0.06});
  slide.addText(text,{x:x+0.08,y:y+0.055,w:w-0.16,h:0.22,fontFace:'Consolas',fontSize:8.6,bold:true,color,align:'center',margin:0,fit:'shrink'});
}
function addCard(slide,x,y,w,h,title,body,opts={}) {
  slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h,rectRadius:0.05,fill:{color:opts.fill||C.panel},line:{color:opts.line||C.line,width:1},radius:0.05});
  if (opts.mark) slide.addText(opts.mark,{x:x+0.22,y:y+0.18,w:0.55,h:0.24,fontFace:'Consolas',fontSize:9,bold:true,color:opts.markColor||C.green2,margin:0});
  slide.addText(title,{x:x+0.22,y:y+(opts.mark?0.52:0.22),w:w-0.44,h:0.34,fontFace:'Aptos Display',fontSize:opts.titleSize||15,bold:true,color:opts.titleColor||C.fg,margin:0,fit:'shrink'});
  slide.addText(body,{x:x+0.22,y:y+(opts.mark?0.9:0.66),w:w-0.44,h:h-(opts.mark?1.08:0.84),fontFace:'Aptos',fontSize:opts.bodySize||11,color:opts.bodyColor||C.muted,margin:0,fit:'shrink',valign:'top'});
}
function addSource(slide, text) {
  slide.addText(text,{x:0.62,y:6.87,w:11.7,h:0.18,fontFace:'Aptos',fontSize:7.2,color:C.dim,margin:0,italic:true,fit:'shrink'});
}
function addNote(slide, text) { slide.addNotes(text); }
function addMetric(slide,x,y,w,label,value,sub,color=C.green) {
  slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h:1.03,rectRadius:0.05,fill:{color:C.panel},line:{color:C.line,width:1},radius:0.05});
  slide.addText(label.toUpperCase(),{x:x+0.15,y:y+0.13,w:w-0.3,h:0.2,fontFace:'Consolas',fontSize:7.8,bold:true,color:C.dim,charSpacing:0.8,margin:0,fit:'shrink'});
  slide.addText(value,{x:x+0.15,y:y+0.33,w:w-0.3,h:0.38,fontFace:'Aptos Display',fontSize:22,bold:true,color,margin:0,fit:'shrink'});
  slide.addText(sub,{x:x+0.15,y:y+0.75,w:w-0.3,h:0.16,fontFace:'Aptos',fontSize:7.4,color:C.muted,margin:0,fit:'shrink'});
}
function addBar(slide,x,y,w,label,val,max=0.6,color=C.green,detail='') {
  slide.addText(label,{x,y:y-0.01,w:1.55,h:0.25,fontFace:'Aptos',fontSize:10.5,bold:true,color:C.fg,margin:0,fit:'shrink'});
  slide.addShape(pptx.ShapeType.roundRect,{x:x+1.62,y,w:w-2.55,h:0.22,rectRadius:0.03,fill:{color:'17251E'},line:{color:'17251E'},radius:0.03});
  const bw=Math.max(0.08,(w-2.55)*(val/max));
  slide.addShape(pptx.ShapeType.roundRect,{x:x+1.62,y,w:bw,h:0.22,rectRadius:0.03,fill:{color},line:{color},radius:0.03});
  slide.addText(val.toFixed(3),{x:x+w-0.83,y:y-0.03,w:0.65,h:0.28,fontFace:'Consolas',fontSize:10,bold:true,color,align:'right',margin:0});
  if(detail) slide.addText(detail,{x:x+1.62,y:y+0.25,w:w-1.85,h:0.16,fontFace:'Aptos',fontSize:7.4,color:C.dim,margin:0,fit:'shrink'});
}

const notes = {
1:`Hello, I’m John Flack. This is ControlSift, my Mentor Me Collective and Google DeepMind AI Research Foundations capstone. The question is simple: can a small language model help a human reviewer tell real cybersecurity proof from paperwork that only looks convincing? For the MMC rubric, the project maps to option 4, Reduced Inequalities; in the United Nations framework, that is Sustainable Development Goal 10. ControlSift is synthetic research, not a production auditor or a replacement for professional judgment.`,
2:`The problem is evidence quality, not document relevance. A policy saying privileged accounts must use multi-factor authentication may be relevant, but it does not prove those accounts were enrolled during the assessment period. NIST SP 800-53A frames control assessment around whether controls are implemented and achieving intended outcomes. NIST also recognizes that smaller organizations often operate with limited cybersecurity resources and budgets. ControlSift therefore tests a low-cost triage approach that could focus human attention without lowering the assurance standard.`,
3:`The objective is a five-class evidence-quality task: Sufficient, Partial, Insufficient, Irrelevant, and Contradictory. The benchmark contains about fifteen hundred synthetic evidence packets, with scenario families isolated across train, validation, test, and challenge splits. Macro F1 is the primary metric so every label counts equally. An early generator let TF-IDF score perfectly by exploiting lexical shortcuts. I treated that as a dataset defect, hardened the benchmark, and sealed the evaluation protocol before final model claims.`,
4:`The solution is a model ladder, not a one-model demo. The classical path compares a majority baseline with TF-IDF logistic regression. The language-model path compares Gemma 3 one-billion-parameter zero-shot, few-shot, and QLoRA adaptation using 4-bit NF4 on free-tier GPU infrastructure. QLoRA was chosen as a memory-efficient fine-tuning method. One boundary matters: the hardened classical runs are dataset version 1.1, while the completed Gemma runs are version 1.0. Those scores are valid experiment receipts, but not a controlled cross-version head-to-head ranking.`,
5:`The results are straightforward. On version 1.1, majority macro F1 is zero point zero six six seven; TF-IDF reaches zero point five three two seven, with challenge macro F1 zero point five two three seven. On version 1.0, Gemma zero-shot reaches zero point zero seven nine six. Few-shot reaches zero point one three six five and is the strongest Gemma run. QLoRA reaches zero point zero eight two seven and does not beat few-shot. Its label parse-success rate is only forty-three point five percent, making output reliability a first-class failure mode. The defensible finding is that few-shot beats QLoRA within the Gemma experiments, and fine-tuning did not automatically improve this task.`,
6:`Responsible AI is built into the design. The corpus is synthetic, so no employer, customer, or patient evidence enters the project. Malformed outputs count as errors instead of being quietly repaired. The public artifact includes a Data Card, Model Card, AI risk register, Intended Use statement, limitations, and a Failure Lab that exposes difficult cases. These choices align with NIST AI Risk Management Framework principles around scope, measurement, human roles, and oversight. Human judgment stays authoritative, and ControlSift makes no production-certification claim.`,
7:`The implementation plan mapped the work across the program’s twelve-week runway, although the technical work finished early. It moved from problem framing and external research, to benchmark generation and hardening, protocol seal, classical baselines, Gemma prompting, QLoRA training, error analysis, and public documentation. Resources were Python, scikit-learn, Gemma 3, Hugging Face, Kaggle or Colab GPU access, and GitHub Pages. Risks included leakage, lexical shortcuts, test-set tuning, fabricated metrics, secret exposure, synthetic-to-real overgeneralization, and automation bias. Mitigations include family-isolated splits, machine-readable results, platform secrets, explicit limitations, and human review. As research and training, the approach is practical, inexpensive, reproducible, and scalable; production use would require governed real-world validation.`,
8:`My recommendation is conservative: do not deploy ControlSift as an audit autopilot. Preserve human authority, improve constrained output handling before stronger model claims, and validate any future operational use on governed real-world evidence. The larger finding is methodological: an AI project does not need an AI victory to be useful. ControlSift preserved a negative fine-tuning result, documented its limits, and left the evidence open for inspection. The finished artifact includes the report, sources, results, Failure Lab, assurance package, reproducibility path, and public site. Thank you for reviewing the work.`
};

{
  const s=pptx.addSlide('MASTER');
  s.background={color:C.bg};
  s.addText('ControlSift',{x:0.62,y:0.95,w:6.25,h:0.78,fontFace:'Aptos Display',fontSize:38,bold:true,color:C.fg,margin:0});
  s.addText('Can a small language model tell proof from paperwork?',{x:0.64,y:1.78,w:6.0,h:1.0,fontFace:'Aptos Display',fontSize:24,color:C.green,margin:0,fit:'shrink'});
  s.addText('AI assurance research for cybersecurity control evidence',{x:0.64,y:2.9,w:5.75,h:0.36,fontFace:'Aptos',fontSize:13.5,color:C.muted,margin:0});
  addPill(s,0.64,3.48,2.8,'MMC OPTION 4 / UN SDG 10',C.panel2,C.green2);
  addPill(s,3.58,3.48,2.68,'SYNTHETIC RESEARCH',C.panel2,C.green);
  s.addShape(pptx.ShapeType.roundRect,{x:7.35,y:0.95,w:5.35,h:5.5,rectRadius:0.06,fill:{color:C.panel},line:{color:C.line,width:1.2},radius:0.06});
  s.addText('ONE CONTROL. TWO VERY DIFFERENT ARTIFACTS.',{x:7.72,y:1.28,w:4.62,h:0.28,fontFace:'Consolas',fontSize:9,bold:true,color:C.dim,charSpacing:0.9,margin:0,fit:'shrink'});
  s.addText('Privileged accounts must use MFA.',{x:7.72,y:1.66,w:4.55,h:0.45,fontFace:'Aptos Display',fontSize:18,bold:true,color:C.fg,margin:0,fit:'shrink'});
  addCard(s,7.72,2.34,4.55,1.38,'Policy document','“Privileged accounts are required to use MFA.”',{mark:'PAPERWORK',markColor:C.amber,titleColor:C.fg,bodySize:10.3});
  addCard(s,7.72,4.05,4.55,1.6,'Operational export','Audit-period IAM rows show the privileged population, MFA enrollment state, and review boundary.',{mark:'PROOF',markColor:C.green2,titleColor:C.fg,bodySize:10.3});
  s.addText('The research question lives in the gap.',{x:7.75,y:5.9,w:4.45,h:0.28,fontFace:'Aptos',fontSize:11.5,bold:true,color:C.green,margin:0,align:'center'});
  addNote(s,notes[1]);
}

{
  const s=pptx.addSlide('MASTER');
  addTitle(s,'01 / Problem identification','Evidence that looks relevant is not always proof','Grounded in control-assessment guidance and real resource constraints.');
  addCard(s,0.62,2.1,4.0,1.42,'Control assessment','NIST SP 800-53A centers assessment on whether controls are implemented and achieve intended outcomes.',{mark:'NIST',markColor:C.green2,bodySize:10.5});
  addCard(s,0.62,3.76,4.0,1.42,'Capacity constraints','NIST small-business guidance recognizes limited budgets, staffing, and specialist capacity.',{mark:'ACCESS',markColor:C.blue,bodySize:10.5});
  s.addText('WHY THIS MATTERS',{x:5.15,y:2.12,w:2.3,h:0.22,fontFace:'Consolas',fontSize:9,bold:true,color:C.dim,charSpacing:1,margin:0});
  const nodes=[{x:5.25,lab:'CONTROL\nCLAIM',sub:'“MFA is required”',col:C.amber},{x:7.5,lab:'EVIDENCE\nPACKET',sub:'policy, export, screenshot…',col:C.blue},{x:9.75,lab:'REVIEW\nJUDGMENT',sub:'does it prove operation?',col:C.green}];
  nodes.forEach((n,i)=>{s.addShape(pptx.ShapeType.roundRect,{x:n.x,y:2.7,w:1.85,h:1.15,rectRadius:0.05,fill:{color:C.panel2},line:{color:n.col,width:1.5},radius:0.05});s.addText(n.lab,{x:n.x+0.12,y:2.92,w:1.61,h:0.45,fontFace:'Consolas',fontSize:11,bold:true,color:n.col,align:'center',margin:0,fit:'shrink'});s.addText(n.sub,{x:n.x+0.1,y:3.43,w:1.65,h:0.24,fontFace:'Aptos',fontSize:7.7,color:C.muted,align:'center',margin:0,fit:'shrink'});if(i<nodes.length-1)s.addShape(pptx.ShapeType.chevron,{x:n.x+1.9,y:3.08,w:0.45,h:0.38,fill:{color:C.dim},line:{color:C.dim}});});
  s.addShape(pptx.ShapeType.roundRect,{x:5.22,y:4.35,w:6.35,h:1.22,rectRadius:0.04,fill:{color:'0A1510'},line:{color:C.line,width:1},radius:0.04});
  s.addText('ControlSift tests whether low-cost triage can focus human attention without lowering the assurance standard.',{x:5.52,y:4.68,w:5.74,h:0.55,fontFace:'Aptos Display',fontSize:16.5,bold:true,color:C.fg,align:'center',margin:0,fit:'shrink'});
  addSource(s,'Sources: NIST SP 800-53A Rev. 5; NIST Small Business Cybersecurity Corner.');
  addNote(s,notes[2]);
}

{
  const s=pptx.addSlide('MASTER');
  addTitle(s,'02 / Research & analysis','A benchmark designed to resist easy answers','Five labels, family-isolated splits, a sealed evaluation protocol, and one useful early failure.');
  const labels=[['SUFFICIENT','complete operational proof',C.green2],['PARTIAL','relevant, but materially incomplete',C.blue],['INSUFFICIENT','on-topic, not execution proof',C.amber],['IRRELEVANT','off-objective substance',C.dim],['CONTRADICTORY','contains a control-failure fact',C.red]];
  const startX=0.62,gap=0.12,w=(12.09-gap*4)/5;
  labels.forEach((d,i)=>{const x=startX+i*(w+gap);s.addShape(pptx.ShapeType.roundRect,{x,y:2.08,w,h:1.2,rectRadius:0.04,fill:{color:C.panel},line:{color:d[2],width:1.1},radius:0.04});s.addText(d[0],{x:x+0.12,y:2.28,w:w-0.24,h:0.25,fontFace:'Consolas',fontSize:9.2,bold:true,color:d[2],align:'center',margin:0,fit:'shrink'});s.addText(d[1],{x:x+0.12,y:2.63,w:w-0.24,h:0.42,fontFace:'Aptos',fontSize:8.4,color:C.muted,align:'center',margin:0,fit:'shrink'});});
  addMetric(s,0.62,3.66,2.52,'Synthetic cases','~1,500','balanced five-class corpus');
  addMetric(s,3.34,3.66,2.52,'Splits','1000 / 200 / 200 / 100','train / val / test / challenge',C.blue);
  addMetric(s,6.06,3.66,2.52,'Primary metric','Macro F1','equal weight to every label',C.green);
  addMetric(s,8.78,3.66,2.52,'Seed','42','deterministic generation',C.amber);
  s.addShape(pptx.ShapeType.roundRect,{x:0.62,y:5.02,w:11.55,h:1.15,rectRadius:0.04,fill:{color:'141B13'},line:{color:C.amber,width:1},radius:0.04});
  s.addText('EARLY FAILURE → BETTER RESEARCH',{x:0.9,y:5.28,w:3.1,h:0.24,fontFace:'Consolas',fontSize:10,bold:true,color:C.amber,charSpacing:0.8,margin:0});
  s.addText('An earlier generator let TF-IDF reach 1.0 by exploiting lexical shortcuts. The benchmark was hardened, then the protocol was sealed before final model claims.',{x:4.02,y:5.2,w:7.75,h:0.55,fontFace:'Aptos',fontSize:11.2,color:C.fg,margin:0,fit:'shrink'});
  addNote(s,notes[3]);
}

{
  const s=pptx.addSlide('MASTER');
  addTitle(s,'03 / Solution development','A model ladder, not a one-model demo','Compare cheap baselines, prompting, and parameter-efficient fine-tuning — while preserving the version boundary.');
  s.addText('CLASSICAL / DATASET v1.1.0',{x:0.72,y:2.08,w:3.6,h:0.22,fontFace:'Consolas',fontSize:9.4,bold:true,color:C.green2,charSpacing:0.8,margin:0});
  const classical=[['Majority','chance floor'],['TF-IDF + LR','lexical baseline']];
  classical.forEach((d,i)=>{const x=0.72+i*2.48;addCard(s,x,2.46,2.2,1.15,d[0],d[1],{mark:`B${i}`,markColor:C.green2,bodySize:9.2,titleSize:14});if(i===0)s.addShape(pptx.ShapeType.chevron,{x:2.99,y:2.83,w:0.34,h:0.34,fill:{color:C.dim},line:{color:C.dim}});});
  s.addText('GEMMA 3 1B / DATASET v1.0.0',{x:6.05,y:2.08,w:4.2,h:0.22,fontFace:'Consolas',fontSize:9.4,bold:true,color:C.blue,charSpacing:0.8,margin:0});
  const gemma=[['Zero-shot','fixed prompt'],['Few-shot','fixed exemplars'],['QLoRA','4-bit NF4 + adapters']];
  gemma.forEach((d,i)=>{const x=6.05+i*2.0;addCard(s,x,2.46,1.78,1.15,d[0],d[1],{mark:`G${i+1}`,markColor:C.blue,bodySize:8.8,titleSize:13.3});if(i<2)s.addShape(pptx.ShapeType.chevron,{x:x+1.83,y:2.83,w:0.27,h:0.34,fill:{color:C.dim},line:{color:C.dim}});});
  s.addShape(pptx.ShapeType.roundRect,{x:0.72,y:4.14,w:11.7,h:1.43,rectRadius:0.05,fill:{color:'131C19'},line:{color:C.amber,width:1.2},radius:0.05});
  s.addText('VERSION BOUNDARY',{x:1.0,y:4.43,w:2.05,h:0.24,fontFace:'Consolas',fontSize:10,bold:true,color:C.amber,charSpacing:0.9,margin:0});
  s.addText('The experiments are real, but the classical and Gemma runs were completed on different benchmark versions. Cross-version values are descriptive receipts — not a controlled head-to-head leaderboard.',{x:3.15,y:4.29,w:8.84,h:0.62,fontFace:'Aptos Display',fontSize:15,bold:true,color:C.fg,margin:0,fit:'shrink'});
  s.addText('Why QLoRA? Memory-efficient fine-tuning makes adaptation possible on constrained hardware and free-tier GPU paths.',{x:3.15,y:4.99,w:8.6,h:0.26,fontFace:'Aptos',fontSize:9.5,color:C.muted,margin:0,fit:'shrink'});
  addSource(s,'Sources: Dettmers et al., “QLoRA” (2023); Google DeepMind / Google, Gemma 3 model documentation.');
  addNote(s,notes[4]);
}

{
  const s=pptx.addSlide('MASTER');
  addTitle(s,'04 / Results','The useful finding is not an automatic AI win','Two internally valid result groups, one important output-reliability failure.');
  s.addShape(pptx.ShapeType.roundRect,{x:0.62,y:2.0,w:5.88,h:3.85,rectRadius:0.05,fill:{color:C.panel},line:{color:C.line,width:1},radius:0.05});
  s.addText('CLASSICAL / v1.1.0',{x:0.92,y:2.28,w:2.8,h:0.24,fontFace:'Consolas',fontSize:10,bold:true,color:C.green2,charSpacing:0.8,margin:0});
  addBar(s,0.92,2.86,5.17,'Majority',0.0667,0.6,C.dim,'challenge 0.0667');
  addBar(s,0.92,3.7,5.17,'TF-IDF + LR',0.5327,0.6,C.green2,'challenge 0.5237');
  s.addText('The hardened v1.1 lexical baseline is no longer trivial, but remains substantial.',{x:0.95,y:4.63,w:5.05,h:0.54,fontFace:'Aptos',fontSize:11,color:C.muted,margin:0,fit:'shrink'});
  s.addShape(pptx.ShapeType.roundRect,{x:6.78,y:2.0,w:5.88,h:3.85,rectRadius:0.05,fill:{color:C.panel},line:{color:C.line,width:1},radius:0.05});
  s.addText('GEMMA 3 1B / v1.0.0',{x:7.08,y:2.28,w:3.1,h:0.24,fontFace:'Consolas',fontSize:10,bold:true,color:C.blue,charSpacing:0.8,margin:0});
  addBar(s,7.08,2.83,5.15,'Zero-shot',0.0796,0.6,C.dim,'parse success 76.0%');
  addBar(s,7.08,3.54,5.15,'Few-shot',0.1365,0.6,C.blue,'parse success 98.5% • strongest Gemma rung');
  addBar(s,7.08,4.25,5.15,'QLoRA',0.0827,0.6,C.amber,'parse success 43.5% • did not beat few-shot');
  s.addShape(pptx.ShapeType.roundRect,{x:0.62,y:6.05,w:12.04,h:0.72,rectRadius:0.04,fill:{color:'101A14'},line:{color:C.line,width:1},radius:0.04});
  s.addText('Defensible conclusion',{x:0.9,y:6.27,w:1.62,h:0.18,fontFace:'Consolas',fontSize:8.7,bold:true,color:C.green,margin:0});
  s.addText('Few-shot beats QLoRA within Gemma v1.0; fine-tuning did not automatically improve the task. Cross-version classical-vs-Gemma ranking is not claimed.',{x:2.58,y:6.18,w:9.65,h:0.34,fontFace:'Aptos',fontSize:10.4,color:C.fg,margin:0,fit:'shrink'});
  addNote(s,notes[5]);
}

{
  const s=pptx.addSlide('MASTER');
  addTitle(s,'05 / Responsible innovation','Assurance includes the failure modes','The project documents how the model can fail, who remains accountable, and what the artifact is not allowed to claim.');
  s.addText('FAILURE LAB / OUTPUT PATH',{x:0.72,y:2.07,w:3.2,h:0.23,fontFace:'Consolas',fontSize:9.4,bold:true,color:C.amber,charSpacing:0.8,margin:0});
  const pipe=[['Evidence packet',C.blue],['Model output',C.blue],['Label parser',C.amber],['Human review',C.green2]];
  pipe.forEach((d,i)=>{const x=0.72+i*1.46;s.addShape(pptx.ShapeType.roundRect,{x,y:2.52,w:1.18,h:0.92,rectRadius:0.04,fill:{color:C.panel2},line:{color:d[1],width:1.2},radius:0.04});s.addText(d[0],{x:x+0.08,y:2.79,w:1.02,h:0.28,fontFace:'Aptos',fontSize:9,bold:true,color:C.fg,align:'center',margin:0,fit:'shrink'});if(i<3)s.addShape(pptx.ShapeType.chevron,{x:x+1.2,y:2.79,w:0.25,h:0.32,fill:{color:C.dim},line:{color:C.dim}});});
  s.addShape(pptx.ShapeType.roundRect,{x:0.72,y:3.86,w:5.55,h:1.44,rectRadius:0.04,fill:{color:'191713'},line:{color:C.amber,width:1},radius:0.04});
  s.addText('QLoRA parse success: 43.5%',{x:1.02,y:4.13,w:2.65,h:0.34,fontFace:'Aptos Display',fontSize:18,bold:true,color:C.amber,margin:0});
  s.addText('Malformed generations count as errors. They are not silently remapped to a favorable label.',{x:1.02,y:4.56,w:4.92,h:0.42,fontFace:'Aptos',fontSize:10.5,color:C.fg,margin:0,fit:'shrink'});
  s.addText('GOVERNANCE ARTIFACTS',{x:6.75,y:2.07,w:3.2,h:0.23,fontFace:'Consolas',fontSize:9.4,bold:true,color:C.green2,charSpacing:0.8,margin:0});
  const gov=[['DATA CARD','what the benchmark is'],['MODEL CARD','what the model is for'],['RISK REGISTER','what can go wrong'],['INTENDED USE','what is allowed'],['LIMITATIONS','what is not proven'],['FAILURE LAB','where it breaks']];
  gov.forEach((d,i)=>{const col=i%2,row=Math.floor(i/2),x=6.75+col*2.8,y=2.48+row*1.03;s.addShape(pptx.ShapeType.roundRect,{x,y,w:2.55,h:0.82,rectRadius:0.035,fill:{color:C.panel},line:{color:C.line,width:1},radius:0.035});s.addText(d[0],{x:x+0.14,y:y+0.12,w:2.27,h:0.2,fontFace:'Consolas',fontSize:8.2,bold:true,color:C.green,margin:0,fit:'shrink'});s.addText(d[1],{x:x+0.14,y:y+0.39,w:2.27,h:0.24,fontFace:'Aptos',fontSize:8.5,color:C.muted,margin:0,fit:'shrink'});});
  s.addText('Human judgment remains authoritative.',{x:7.0,y:5.82,w:5.05,h:0.34,fontFace:'Aptos Display',fontSize:18,bold:true,color:C.green2,align:'center',margin:0});
  addSource(s,'Responsible-AI grounding: NIST AI Risk Management Framework and NIST Generative AI Profile.');
  addNote(s,notes[6]);
}

{
  const s=pptx.addSlide('MASTER');
  addTitle(s,'06 / Implementation plan','Built to be practical, inspectable, and reproducible','A six-phase path, modest infrastructure, explicit risks, and clear production boundaries.');
  const phases=['Frame','Build','Harden + seal','Run ladder','Analyze','Publish'];
  phases.forEach((p,i)=>{const x=0.7+i*2.05;s.addShape(pptx.ShapeType.ellipse,{x,y:2.12,w:0.52,h:0.52,fill:{color:i===5?C.green2:C.panel2},line:{color:C.green2,width:1}});s.addText(String(i+1),{x:x,y:2.24,w:0.52,h:0.18,fontFace:'Consolas',fontSize:9,bold:true,color:i===5?C.bg:C.green2,align:'center',margin:0});s.addText(p,{x:x-0.35,y:2.76,w:1.22,h:0.28,fontFace:'Aptos',fontSize:9.2,bold:true,color:C.fg,align:'center',margin:0,fit:'shrink'});if(i<5)s.addShape(pptx.ShapeType.line,{x:x+0.55,y:2.38,w:1.5,h:0,line:{color:C.line,width:2}});});
  s.addText('12-week program runway • technical work completed early',{x:0.72,y:3.2,w:11.6,h:0.24,fontFace:'Consolas',fontSize:8.8,color:C.dim,align:'center',margin:0});
  addCard(s,0.72,3.72,3.75,2.15,'Resources','Python • scikit-learn • Gemma 3 • Hugging Face • Kaggle / Colab • GitHub Pages',{mark:'BUILD',markColor:C.blue,bodySize:11,titleSize:16});
  addCard(s,4.78,3.72,3.75,2.15,'Risks managed','Leakage • lexical shortcuts • test tuning • fabricated metrics • secret exposure • automation bias',{mark:'RISK',markColor:C.amber,bodySize:10.6,titleSize:16});
  addCard(s,8.84,3.72,3.75,2.15,'Viability','Practical: low-cost baseline\nSustainable: synthetic + open\nScalable: research / training\nProduction: validation required',{mark:'IMPACT',markColor:C.green2,bodySize:10.2,titleSize:16});
  addNote(s,notes[7]);
}

{
  const s=pptx.addSlide('MASTER');
  addTitle(s,'07 / Conclusion','A useful AI project does not need an AI victory','The value is in the evidence, the boundaries, and the decision the experiment supports.');
  s.addShape(pptx.ShapeType.roundRect,{x:0.72,y:2.08,w:8.15,h:3.88,rectRadius:0.05,fill:{color:C.panel},line:{color:C.line,width:1},radius:0.05});
  const takes=[['1','Do not deploy it as audit autopilot.','Human authority and governed validation remain mandatory.'],['2','Few-shot beat QLoRA within the Gemma v1.0 runs.','Fine-tuning did not automatically improve this evidence task.'],['3','The negative result is still a result.','ControlSift preserves the receipts, failure modes, and claim boundaries.']];
  takes.forEach((d,i)=>{const y=2.43+i*1.03;s.addShape(pptx.ShapeType.ellipse,{x:1.02,y,w:0.48,h:0.48,fill:{color:i===2?C.green2:C.panel2},line:{color:C.green2,width:1}});s.addText(d[0],{x:1.02,y:y+0.12,w:0.48,h:0.17,fontFace:'Consolas',fontSize:9,bold:true,color:i===2?C.bg:C.green2,align:'center',margin:0});s.addText(d[1],{x:1.7,y:y-0.01,w:6.65,h:0.32,fontFace:'Aptos Display',fontSize:15.5,bold:true,color:C.fg,margin:0,fit:'shrink'});s.addText(d[2],{x:1.7,y:y+0.39,w:6.55,h:0.26,fontFace:'Aptos',fontSize:9.6,color:C.muted,margin:0,fit:'shrink'});});
  s.addText('INSPECT THE FULL ARTIFACT',{x:9.28,y:2.18,w:3.0,h:0.22,fontFace:'Consolas',fontSize:9.3,bold:true,color:C.green2,charSpacing:0.8,align:'center',margin:0});
  const qr='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAADA0lEQVR4nO2cUY6jMAyGPy9IfQzSHKBHCTfYI432SHMDOEoPsBJ5rBTkfUhC092n2XYGCu5DVQGfiFXXsX+bivLp1/jj8wwYZJBBBhlkkEH7hCS/Whg7kD606Y1RWiCUC/pVlmfQN0KoqipeVVWnRoFGdaBRcKr4qUknquuGjdtk0DOgsAQAdxXpXUzHGM8R6YEUQdZankErQqEFP82SgsJX3smgV4BUJ9BfHSmF0IFZdPiKOxm0TajsBE6BAOBiC+Gk4qc3gEbFf0AdLjZuk0GPQNkjRgGgQfzH2+IMIP7SRmCWdZZn0LdDySOqADCeI+VYBJhF7yPE5m0y6BHo3+rT5XxSBxdTWkGuSPPFVn3uGip5ROhQ3FWU0EYldOCnOZ1TgHrb2LhNBj0CUYrMJqlR+ZNGkjg1LCf8ZDHiCNCya0TAadEnk0i5uIWLkF3FPGLnUP7Z6xIFBqdFxS4uUIUHixG7h+4yS413DqKl6tAJkkxlMWL3UPGICUpXC4qDLK0tLI84DFS+ZHcfIzRSdTxzRWp5xHEgeb+0SB9OCsySPo3nq5DlylnAxbWWZ9AamSWkyJDqivLtF5lqqUMtRhwEGrtGRaRFeiCnFRqB0CK99TWOAy1TMLMozK0SyqFRAK9zq4QmStXu2rhNBj0OyfuUpysZu0YhnLIUAY2KnOud5EVsMujh6jPlDANLhUFWIVJu4UvpYXnEMaBG80CdRkS6Weo2x6VFB3e1XeMAUJ1HeAXGn79bsoOA+KmT0vtsypTExm0y6BGo6n3eJKkiXEZKMgF5WN92jb1DdQcr65N5Tka19ENLu8v0iONAt2e6dABycRFOqnoRIVeky1T2S9hk0EOQX/aK7Act0rvr8lRPTI//rbU8g74fuj3TVXoYOqQ2R6OMInIbwHwZmwx6CuQnYJSTSu+upb/l8lS29Gsvz6AVoEalh3qbyNMTT7+TQRuE/p7OvxUc1bFlztI0y/1Dix4BVBoUxQ98ma+r5mnMI/YMif0zmUEGGWSQQQYZ9J/QH3/uexdCEoBoAAAAAElFTkSuQmCC';
  s.addImage({data:qr,x:9.62,y:2.65,w:2.28,h:2.28});
  s.addText('jtflack-grc.github.io/controlsift/',{x:9.13,y:5.12,w:3.26,h:0.3,fontFace:'Consolas',fontSize:9,color:C.fg,align:'center',margin:0,fit:'shrink'});
  s.addText('Report • sources • results • Failure Lab • assurance • reproduce',{x:9.2,y:5.5,w:3.1,h:0.5,fontFace:'Aptos',fontSize:9.2,color:C.muted,align:'center',margin:0,fit:'shrink'});
  addSource(s,'External grounding and full bibliography are published in the ControlSift capstone research-sources page.');
  addNote(s,notes[8]);
}

const out = process.env.CONTROLSIFT_DECK_OUT || path.resolve(__dirname, '../docs/capstone/submit/ControlSift_Capstone_Slides.pptx');
await pptx.writeFile({ fileName: out });
console.log(`Wrote ${out}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
