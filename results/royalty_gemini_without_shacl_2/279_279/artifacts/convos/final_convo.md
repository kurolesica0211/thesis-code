================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Pavlos, Crown Prince of Greece, Prince of Denmark (Greek: Παύλος Ντε Γκρες, romanized: Pavlos de Grèce; born 20 May 1967), is a Greek financier who is the former heir apparent to the defunct throne of Greece, becoming the Head of the Royal House of Greece upon his father's death on 10 January 2023.
Pavlos was Crown Prince of Greece and heir apparent to the Greek throne from birth until the monarchy's abolition.
Pavlos was born in Athens as the second child and eldest son of the last King of Greece, Constantine II, and his wife Queen Anne-Marie.
Pavlos was born into an unstable era for Greek politics, just shy of turning eight months old when he and his family were sent into exile, after Constantine II staged a failed counter-coup against the military junta.
They first lived in Rome, before eventually settling in Copenhagen, where his family lived with Pavlos's maternal grandparents, King Frederik IX and Queen Ingrid of Denmark.
Although they were in exile since December 1967, his parents continued to officially reign as King and Queen of the Hellenes from 1967 until 1973, when the military junta abolished the Greek monarchy and established the Third Hellenic Republic as its successor state.
Following the abolition of the monarchy, Pavlos and his siblings grew up in London.
On 1 July 1995, Pavlos married Marie-Chantal Miller.
They have five children: Maria-Olympia, Constantine-Alexios, Achileas-Andreas, Odysseas-Kimon, and Aristides-Stavros.
Pavlos is closely related to many European royals.
Queens Margrethe II of Denmark and Sofía of Spain are his aunts, and Kings Felipe VI of Spain and Frederik X of Denmark are his first cousins.
Early life

Pavlos was born on 20 May 1967 at the Tatoi Palace north of Athens, used at the time as the secondary residence of the Greek royal family.
He was the second child and first son of King Constantine II and Queen Anne-Marie of Greece.
Constantine II had ascended the throne on 6 March 1964, aged 23, following the death of his father and predecessor, Paul, so Pavlos was crown prince from birth.
His mother is the youngest sister of the Danish queen Margrethe II, and his father was the brother of Sofía, the former queen consort of Spain.
His maternal grandparents were Frederik IX of Denmark and his queen consort, Ingrid of Sweden.
Pavlos displaced his older sister, Alexia, as heir to the throne due to Greece's order of succession adhering to male-preference primogeniture.
Crown Prince

Pavlos was born into a turbulent era in Greek politics, barely a month after a coup d'état which ended democratic rule in Greece over the king's objections on 21 April 1967, ushering in a military junta, led by Georgios Papadopoulos.
In December of that year, Constantine attempted a counter-coup that failed due to planning mistakes, leaks, and insufficient military support.
Pursued by the junta, Constantine fled with his wife, children, mother and sister to Rome.
They then went to Copenhagen and lived with Anne-Marie's mother, Queen Ingrid.
From 1967 to 1973, Greece officially remained a monarchy, with a regency appointed while the king lived in exile.
Following the discovery and suppression of a "wide-ranging" anti-junta movement, just before its outbreak, among the ranks of the mostly royalist Navy, Papadopoulos, on 1 June 1973, declared Greece a presidential republic with himself as president and proclaimed a referendum for 29 July 1973 on the issue of the monarchy.
The referendum was held without opposition and its result confirmed the regime change, with Constantine becoming "officially" deposed.
On 17 November 1974, after the fall of the dictatorship, the 1974 Greek legislative election was held, resulting in a victory for Constantine Karamanlis and his New Democracy party.
Constantine announced that he "respects" the "decision of the Greek people."
He and Anne-Marie had been living with their family in London for several years.
Pavlos's youngest siblings were born in London: Theodora in 1983 and Philippos in 1986.
Pavlos was educated at the Hellenic College of London, founded by his parents in 1980.
On 11 May 1994, the Greek Government under prime-minister Andreas Papandreou renounced the Greek-citizenship status of Pavlos, alongside Constantine, and the rest of the former royal family through law 2215/1994.
The law stated that Constantine's Greek-citizenship status, and accordingly his family's, could only be restored under specific conditions, including the selection of an explicit surname.
The following year, while sharing a house in Washington, DC, he and his cousin, Felipe VI of Spain, then Prince of Asturias, attended Georgetown University, where both obtained a Master of Science in Foreign Service.
After, Pavlos lived between New York City and London, working as an investment consultant.
Head of the Greek royal family

Following the death of his father on 10 January 2023, Pavlos delivered Constantine's eulogy during the funeral ceremony and carried his coffin with his brothers, sons and nephews at the burial.
A rumour circulated that Pavlos intended to permanently relocate to Greece, but this was later denied by the spokesperson of the former Greek royal family, Ivi Macris, as "completely false".
On 22 January, Pavlos spoke to French magazine Point de Vue regarding his new role.
In the interview, Pavlos thanked the public for their respect towards the Greek royal family and said that those who crowded the funeral, whether they were "monarchists or not", "paid tribute to a historical personality, a part of Greek history."
When asked about the role he sees himself upholding in Greek society, Pavlos explained that he would "not take on an official role", but will "uphold the family's exemplary."
He added that his eldest son Constantine-Alexios would not take on any official role either, but would "follow his grandfather's example and be a good man."
Pavlos issued a statement about the Tempi train collision in February 2023, which caused the death of almost 60 people, styling himself Head of the former Royal House of Greece following Constantine's death.
The statement read: "Today all of Greece is mourning.
Pavlos also thanked the rescue and medical teams involved for their "superhuman efforts", before giving his "heartbroken" condolences to the families who lost their children in the accident and asking God to bless them all.
Soon after, as Pavlos was leaving Athens that month, it was revealed that he and his family had been searching for a home in Greece, with Pavlos telling journalists that he had not "found a house yet".
In April 2023, Pavlos attended a Greek Orthodox Easter service in the Hamptons, where his sons Constantine-Alexios and Odysseas-Kimon were holding the Epitaphios.
Pavlos attended the coronation of Charles III and Camilla in May with his mother and wife.
On 3 July 2023 at 11:45pm, Pavlos and his brother, Nikolaos, appeared in a special edition of 365 Moments, a Greek television series hosted by Sofia Papaioannou.
The episode marked the first interview with Pavlos and Nikolaos since their father's death, and it discussed the passing of their father, their stripped Greek citizenship and their surname.
Pavlos described his father as "strict but very loving" and said that despite being forced into exile, he still wanted to help his family.
Pavlos also announced that he was now living in Greece again, which is what he "always wanted to".
He explained that the opportunity to live in Greece occurred as his job allowed for overseas work.
When asked whether he accepted the last name "Glücksburg", Pavlos said that he would never see it as his name.
Denmark's family name is not that.
He explained that throughout his life, he never introduced himself with a last name, but rather called himself "Pavlos of Greece".
Pavlos also added that he was "very interested in  politics", but would never become involved, has no political association and would always long for his Greek passport to be returned.
Pavlos and Marie-Chantal attended the 2023 British Fashion Awards.
There, Pavlos was spotted with a black eye patch covering his left eye.
The day prior, Marie-Chantal posted to Instagram a close-up photo of his eye patch, saying, "Hopefully a temporary new look, but he’s kind of cute".
Following worry online, Pavlos announced on Instagram that he had undergone a retinal detachment surgery.
After thanking people for their support and wishes, Pavlos explained that the surgery was "successful", however he would be unable to travel and therefore have to spend Christmas in London.
Between January and February 2024, Pavlos and his family attended three memorial services to mark the one year anniversary of Constantine's death — one in Athens and two in London, including a thanksgiving service.
After a memorial service the following day, Pavlos and Nikolaos were interviewed by ANT1 reporter Isaac Karipidis.
On 28 September 2024, Pavlos served as a groomsman at the wedding of Princess Theodora and Matthew Kumar at the Metropolitan Cathedral.
On 19 December 2024, Pavlos, his five children and his four siblings submitted an application for Greek citizenship, which had been stripped from the family in 1994.
Pavlos's mother, Anne-Marie, did not apply, as she was reportedly "not interested".
Under law, Pavlos and his family, in order to receive citizenship, must pledge allegiance to the republican constitution and adopt a surname.
Ultimately, the surname of "Ντε Γκρες" (transliteration of De Grèce, meaning "of Greece") was chosen.
It was reported by the royal family that this surname was chosen as it was the one used by the late Prince Michael of Greece and Denmark, and so was the "only familiar one" to them.
The following day, Pavlos's citizenship, alongside that of his children and siblings, was reinstated according to the provisions of the 1994 law by order of the Minister of the Interior, Theodoros Livanios.
Deputy Minister Pavlos Marinakis said to Action 24 that the ex-royal family's "request was made in accordance with the law", while the left-wing SYRIZA party stated "the choice of family name is problematic".
The Communist Party of Greece and PASOK also criticized the government's decision.
Personal life

Pavlos married American heiress Marie-Chantal Miller, whom he had met at a party three years earlier in New Orleans, on 1 July 1995.
After their marriage, the couple took up residence in Greenwich, Connecticut, the job that Pavlos obtained with the Charles R. Weber ship-broking company being headquartered there.
The couple has five children: Maria-Olympia (b. 1996), Constantine-Alexios (b. 1998), Achileas-Andreas (b. 2000), Odysseas-Kimon (b. 2004), and Aristidis-Stavros (b. 2008).
Pavlos is a bluewater yachtsman and crews on the multi-record-breaking monohull Mari-Cha IV, owned by his father-in-law;
businessman Robert W. Miller.


Titles, styles, and honours

From birth, Pavlos was the heir apparent to the throne of Greece and as such he was referred to as the Crown Prince of Greece with the style of Royal Highness.
Through his male-line descent from Christian IX of Denmark, he is also a Prince of Denmark with the style of Highness.
Dynastic orders

Foreign honours

Ancestry

Pavlos is a direct descendant of three reigning sovereign monarchs at birth.
He is the eldest son of the King of Greece, grandson of the King of Denmark and great-grandson of the King of Sweden, all living and enthroned when he was born.
His paternal aunt, Sofía, was Queen consort of Spain and his paternal first cousin, Felipe VI, is the current King of Spain.
His maternal aunt, Margrethe II, was the reigning Queen of Denmark and his maternal first cousin, Frederik X, is the current King of Denmark.
Pavlos's parents, grandparents and great-grandparents were all reigning monarchs and consorts.
Pavlos is a scion multiple times of Queen Victoria and King Christian IX, who were dubbed the "grandmother of Europe" and "father-in-law of Europe" respectively, due to royal intermarriage.
As a result, he descends from Christian IX of Denmark through three of his children; in the male line through his second son, George I of Greece, in the female line through his eldest son, Frederik VIII of Denmark, and through King Christian's youngest daughter, Princess Thyra.
He also descends thrice from Queen Victoria; once through her third son, Prince Arthur, and twice through her eldest daughter, Victoria, Princess Royal.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns1:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns2:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns2:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (dd75f592-2efe-4e6d-b1e0-01f1e2769980)
 Call ID: dd75f592-2efe-4e6d-b1e0-01f1e2769980
  Args:
    source: Pavlos
    type: :Man
  AssignClass (c9ce92d3-5416-4ef6-9a63-277ccca60d6e)
 Call ID: c9ce92d3-5416-4ef6-9a63-277ccca60d6e
  Args:
    source: Constantine_II
    type: :Man
  AssignClass (45406b32-a104-4394-87d5-48a10393d914)
 Call ID: 45406b32-a104-4394-87d5-48a10393d914
  Args:
    type: :Woman
    source: Anne-Marie
  AssignClass (ac65dac0-cab9-4000-9f3c-15c7cd75a9d1)
 Call ID: ac65dac0-cab9-4000-9f3c-15c7cd75a9d1
  Args:
    type: :Woman
    source: Marie-Chantal_Miller
  AssignClass (0b5476b8-cdf3-40be-80a8-01c8498ef4c4)
 Call ID: 0b5476b8-cdf3-40be-80a8-01c8498ef4c4
  Args:
    type: :Woman
    source: Maria-Olympia
  AssignClass (cb2bd7e3-0ff7-47b8-b81b-84d574694581)
 Call ID: cb2bd7e3-0ff7-47b8-b81b-84d574694581
  Args:
    type: :Man
    source: Constantine-Alexios
  AssignClass (0181be30-8266-42a9-9feb-6a6ae664beb0)
 Call ID: 0181be30-8266-42a9-9feb-6a6ae664beb0
  Args:
    source: Achileas-Andreas
    type: :Man
  AssignClass (eb3d0d34-10a2-4f16-b728-79261f4229fe)
 Call ID: eb3d0d34-10a2-4f16-b728-79261f4229fe
  Args:
    source: Odysseas-Kimon
    type: :Man
  AssignClass (d4f170a6-6562-4012-81b8-934e91fc9123)
 Call ID: d4f170a6-6562-4012-81b8-934e91fc9123
  Args:
    source: Aristides-Stavros
    type: :Man
  AssignClass (ebfc4a21-f713-4491-a896-092ab5c7992d)
 Call ID: ebfc4a21-f713-4491-a896-092ab5c7992d
  Args:
    type: :Woman
    source: Sofía_of_Spain
  AssignClass (b401c7b9-7774-4091-abc5-f1f0ffbbd259)
 Call ID: b401c7b9-7774-4091-abc5-f1f0ffbbd259
  Args:
    source: Margrethe_II_of_Denmark
    type: :Woman
  AssignClass (7c343301-9753-45e2-9e1e-18510818f69b)
 Call ID: 7c343301-9753-45e2-9e1e-18510818f69b
  Args:
    source: Frederik_IX_of_Denmark
    type: :Man
  AssignClass (365bef33-d083-4d4f-8af3-c661d1883ac4)
 Call ID: 365bef33-d083-4d4f-8af3-c661d1883ac4
  Args:
    source: Ingrid_of_Sweden
    type: :Woman
  AssignClass (906278da-e4ca-4eb2-9be3-eebe36be1442)
 Call ID: 906278da-e4ca-4eb2-9be3-eebe36be1442
  Args:
    source: Paul_of_Greece
    type: :Man
  AssignClass (4a6e0883-a952-46a5-80eb-7611578ff054)
 Call ID: 4a6e0883-a952-46a5-80eb-7611578ff054
  Args:
    type: :Woman
    source: Alexia_of_Greece
  AssignClass (f09891f8-ae96-4567-8e73-b7d9e2445e43)
 Call ID: f09891f8-ae96-4567-8e73-b7d9e2445e43
  Args:
    type: :Woman
    source: Theodora_of_Greece
  AssignClass (f843e53e-db04-46d5-b606-0e6dd9006eca)
 Call ID: f843e53e-db04-46d5-b606-0e6dd9006eca
  Args:
    source: Philippos_of_Greece
    type: :Man
  AssignClass (00d6d558-ff6a-4f75-b1cd-2925c26197cf)
 Call ID: 00d6d558-ff6a-4f75-b1cd-2925c26197cf
  Args:
    source: Nikolaos_of_Greece
    type: :Man
  AssignClass (4ba73cda-fe30-41b6-93ee-caeeedc40b6c)
 Call ID: 4ba73cda-fe30-41b6-93ee-caeeedc40b6c
  Args:
    source: Michael_of_Greece
    type: :Man
  AssignClass (7754d550-a9da-45fa-b1e1-252a5c9d9465)
 Call ID: 7754d550-a9da-45fa-b1e1-252a5c9d9465
  Args:
    type: :Woman
    source: Marina_of_Greece
  AssignClass (7917f0ec-deb7-4545-a915-25cdccc57a93)
 Call ID: 7917f0ec-deb7-4545-a915-25cdccc57a93
  Args:
    type: :Man
    source: Felipe_VI_of_Spain
  AssignClass (641f0707-3a95-4a5d-8cb0-494ac30f5c22)
 Call ID: 641f0707-3a95-4a5d-8cb0-494ac30f5c22
  Args:
    source: Frederik_X_of_Denmark
    type: :Man
  AddLiteral (9c09efe9-7224-4f95-9dac-0b1860b33938)
 Call ID: 9c09efe9-7224-4f95-9dac-0b1860b33938
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Pavlos
    literal_value: 1967
  AddTriple (1b59d402-d31c-4015-8d69-af60ea822f77)
 Call ID: 1b59d402-d31c-4015-8d69-af60ea822f77
  Args:
    source: Pavlos
    target: Constantine_II
    relation: :hasFather
  AddTriple (41d16659-c36e-4918-81a6-acf521fdc2b7)
 Call ID: 41d16659-c36e-4918-81a6-acf521fdc2b7
  Args:
    relation: :hasMother
    source: Pavlos
    target: Anne-Marie
  AddTriple (5ea0d4e1-169a-4f53-aa77-e87458f76a9c)
 Call ID: 5ea0d4e1-169a-4f53-aa77-e87458f76a9c
  Args:
    source: Constantine_II
    target: Paul_of_Greece
    relation: :hasFather
  AddTriple (64621a19-43bd-4043-bdb1-2615cf8e249e)
 Call ID: 64621a19-43bd-4043-bdb1-2615cf8e249e
  Args:
    source: Pavlos
    target: Anne-Marie
    relation: :hasMother
  AddTriple (cb0e0b2a-536f-4526-a770-0c00f136c43c)
 Call ID: cb0e0b2a-536f-4526-a770-0c00f136c43c
  Args:
    source: Anne-Marie
    target: Frederik_IX_of_Denmark
    relation: :hasFather
  AddTriple (109f6f6d-8220-41c6-a5d3-b5fe977386b1)
 Call ID: 109f6f6d-8220-41c6-a5d3-b5fe977386b1
  Args:
    source: Anne-Marie
    target: Ingrid_of_Sweden
    relation: :hasMother
  AddTriple (071a347d-017c-4abd-99fc-8d961d91fff1)
 Call ID: 071a347d-017c-4abd-99fc-8d961d91fff1
  Args:
    source: Pavlos
    target: Anne-Marie
    relation: :hasMother
  AddTriple (a7477c9d-53ec-45b1-9d78-51901b2ddab1)
 Call ID: a7477c9d-53ec-45b1-9d78-51901b2ddab1
  Args:
    relation: :hasFather
    target: Constantine_II
    source: Pavlos
  AddTriple (deecc492-2484-4bbb-bcd2-1836dd211237)
 Call ID: deecc492-2484-4bbb-bcd2-1836dd211237
  Args:
    relation: :hasFather
    target: Pavlos
    source: Constantine-Alexios
  AddTriple (0d5e2a26-e7d6-4552-87fc-faa1540f4b1f)
 Call ID: 0d5e2a26-e7d6-4552-87fc-faa1540f4b1f
  Args:
    relation: :hasMother
    target: Marie-Chantal_Miller
    source: Constantine-Alexios
  AddTriple (be1a11d5-c373-4f90-aac7-16fdebecf3bc)
 Call ID: be1a11d5-c373-4f90-aac7-16fdebecf3bc
  Args:
    relation: :hasFather
    target: Pavlos
    source: Maria-Olympia
  AddTriple (041aeb80-0149-41e8-91bf-e897e5c05baf)
 Call ID: 041aeb80-0149-41e8-91bf-e897e5c05baf
  Args:
    source: Maria-Olympia
    target: Marie-Chantal_Miller
    relation: :hasMother
  AddTriple (79a4fd34-fb64-4bfb-89c0-051a52b39397)
 Call ID: 79a4fd34-fb64-4bfb-89c0-051a52b39397
  Args:
    source: Achileas-Andreas
    target: Pavlos
    relation: :hasFather
  AddTriple (7bb25f55-07e6-441e-a4a4-62d5222a69ce)
 Call ID: 7bb25f55-07e6-441e-a4a4-62d5222a69ce
  Args:
    target: Marie-Chantal_Miller
    source: Achileas-Andreas
    relation: :hasMother
  AddTriple (78d25dd0-2c1a-4f6d-8557-0f5ff1de00c9)
 Call ID: 78d25dd0-2c1a-4f6d-8557-0f5ff1de00c9
  Args:
    target: Pavlos
    source: Odysseas-Kimon
    relation: :hasFather
  AddTriple (70ade827-6287-406c-a487-1d0194c55d6f)
 Call ID: 70ade827-6287-406c-a487-1d0194c55d6f
  Args:
    relation: :hasMother
    target: Marie-Chantal_Miller
    source: Odysseas-Kimon
  AddTriple (3c4a6ef0-0d50-400f-91ce-cb9adb0312f3)
 Call ID: 3c4a6ef0-0d50-400f-91ce-cb9adb0312f3
  Args:
    relation: :hasFather
    target: Pavlos
    source: Aristides-Stavros
  AddTriple (8c6cac52-f7d2-4308-b147-aef9645bd4e5)
 Call ID: 8c6cac52-f7d2-4308-b147-aef9645bd4e5
  Args:
    source: Aristides-Stavros
    target: Marie-Chantal_Miller
    relation: :hasMother
  AddTriple (bd12f943-3c1b-4e00-b95c-47f8fadf4597)
 Call ID: bd12f943-3c1b-4e00-b95c-47f8fadf4597
  Args:
    relation: :isSisterOf
    source: Alexia_of_Greece
    target: Pavlos
  AddTriple (939cba91-61dc-4cf9-a7bc-01c53af4f1f3)
 Call ID: 939cba91-61dc-4cf9-a7bc-01c53af4f1f3
  Args:
    relation: :isSisterOf
    target: Pavlos
    source: Theodora_of_Greece
  AddTriple (6f0e5950-4154-4279-a173-67babfff3509)
 Call ID: 6f0e5950-4154-4279-a173-67babfff3509
  Args:
    relation: :isBrotherOf
    target: Pavlos
    source: Philippos_of_Greece
  AddTriple (b360fabf-b3b2-451c-8538-ea6225aba455)
 Call ID: b360fabf-b3b2-451c-8538-ea6225aba455
  Args:
    relation: :isBrotherOf
    target: Pavlos
    source: Nikolaos_of_Greece
  AddTriple (a8ab69a7-5e76-4033-9750-d2d44c42f5b5)
 Call ID: a8ab69a7-5e76-4033-9750-d2d44c42f5b5
  Args:
    relation: :isSisterOf
    target: Constantine_II
    source: Sofía_of_Spain
  AddTriple (9c1d2970-f221-41e0-b846-e88a90abd3ed)
 Call ID: 9c1d2970-f221-41e0-b846-e88a90abd3ed
  Args:
    relation: :isSisterOf
    target: Anne-Marie
    source: Margrethe_II_of_Denmark
  Finish (f630abaf-fbfb-4a8c-9aee-d719e3cad294)
 Call ID: f630abaf-fbfb-4a8c-9aee-d719e3cad294
  Args: