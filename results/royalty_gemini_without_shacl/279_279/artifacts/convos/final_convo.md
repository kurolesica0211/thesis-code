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
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns1:Variable .

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

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (ee578969-4c03-41f7-b29f-1d09823b8796)
 Call ID: ee578969-4c03-41f7-b29f-1d09823b8796
  Args:
    source: :Pavlos
    type: :Man
  AssignClass (23011259-0d8c-4f01-9ed9-34e9cd7a6733)
 Call ID: 23011259-0d8c-4f01-9ed9-34e9cd7a6733
  Args:
    source: :Pavlos
    type: :Person
  AddLiteral (0711263e-2606-452b-b6c3-c8a04036c551)
 Call ID: 0711263e-2606-452b-b6c3-c8a04036c551
  Args:
    literal_type: xsd:integer
    literal_value: 1967
    relation: :hasBirthYear
    source: :Pavlos
  AssignClass (f2a8e12b-26e8-411d-8b95-fed3b47141d6)
 Call ID: f2a8e12b-26e8-411d-8b95-fed3b47141d6
  Args:
    source: :ConstantineII
    type: :Man
  AssignClass (9041ee22-0d21-43ac-9f4c-64fac930bece)
 Call ID: 9041ee22-0d21-43ac-9f4c-64fac930bece
  Args:
    source: :ConstantineII
    type: :Person
  AddTriple (efe81b3e-5b8e-42d6-8c70-29e4f55ab608)
 Call ID: efe81b3e-5b8e-42d6-8c70-29e4f55ab608
  Args:
    relation: :hasFather
    target: :ConstantineII
    source: :Pavlos
  AssignClass (de8967bc-0c68-4903-9d56-3195f8596ebb)
 Call ID: de8967bc-0c68-4903-9d56-3195f8596ebb
  Args:
    source: :Anne-Marie
    type: :Woman
  AssignClass (87696d59-34e0-44b0-b23e-d1dd896164dd)
 Call ID: 87696d59-34e0-44b0-b23e-d1dd896164dd
  Args:
    source: :Anne-Marie
    type: :Person
  AddTriple (b0c08361-c696-4cc2-b267-c3d58497ba17)
 Call ID: b0c08361-c696-4cc2-b267-c3d58497ba17
  Args:
    target: :Anne-Marie
    source: :Pavlos
    relation: :hasMother
  AddTriple (8843ff49-8c06-492a-a2a4-ab9eeea698da)
 Call ID: 8843ff49-8c06-492a-a2a4-ab9eeea698da
  Args:
    relation: :hasMarriageYear
    target: :Marie-ChantalMiller
    source: :Pavlos
  AddLiteral (e2ef4503-124c-476f-877a-35968236d55e)
 Call ID: e2ef4503-124c-476f-877a-35968236d55e
  Args:
    literal_type: xsd:integer
    source: :Pavlos
    relation: :hasMarriageYear
    literal_value: 1995
  AssignClass (4d124142-ae98-41f9-8a2b-049204305296)
 Call ID: 4d124142-ae98-41f9-8a2b-049204305296
  Args:
    source: :Marie-ChantalMiller
    type: :Woman
  AssignClass (05c502b3-536b-4f5d-ab66-27d8a6240755)
 Call ID: 05c502b3-536b-4f5d-ab66-27d8a6240755
  Args:
    source: :Marie-ChantalMiller
    type: :Person
  AddTriple (0a1ee2e0-01c8-4708-a44e-03693be5188e)
 Call ID: 0a1ee2e0-01c8-4708-a44e-03693be5188e
  Args:
    relation: :hasChild
    target: :Maria-Olympia
    source: :Pavlos
  AddTriple (99576a76-4828-4e40-85e8-b1233cd836c7)
 Call ID: 99576a76-4828-4e40-85e8-b1233cd836c7
  Args:
    relation: :hasChild
    source: :Pavlos
    target: :Constantine-Alexios
  AddTriple (ccb1ea15-6407-43e2-81a2-108094463d72)
 Call ID: ccb1ea15-6407-43e2-81a2-108094463d72
  Args:
    target: :Achileas-Andreas
    source: :Pavlos
    relation: :hasChild
  AddTriple (27327366-1fb9-434b-97b9-3386f2a27a44)
 Call ID: 27327366-1fb9-434b-97b9-3386f2a27a44
  Args:
    relation: :hasChild
    target: :Odysseas-Kimon
    source: :Pavlos
  AddTriple (4694797e-0a11-4556-ae05-2ce46fbb746e)
 Call ID: 4694797e-0a11-4556-ae05-2ce46fbb746e
  Args:
    relation: :hasChild
    source: :Pavlos
    target: :Aristides-Stavros
  AssignClass (1f1426cf-5209-418c-9445-33a66eb4b9d1)
 Call ID: 1f1426cf-5209-418c-9445-33a66eb4b9d1
  Args:
    source: :Maria-Olympia
    type: :Woman
  AssignClass (4defaf46-470d-4ba1-b7c5-ce1b60fc517f)
 Call ID: 4defaf46-470d-4ba1-b7c5-ce1b60fc517f
  Args:
    source: :Constantine-Alexios
    type: :Man
  AssignClass (c60511d8-1d3e-4f85-ade7-ea2bb20042bf)
 Call ID: c60511d8-1d3e-4f85-ade7-ea2bb20042bf
  Args:
    source: :Achileas-Andreas
    type: :Man
  AssignClass (1e91d666-65f6-4fbf-b198-0441f8c948f0)
 Call ID: 1e91d666-65f6-4fbf-b198-0441f8c948f0
  Args:
    source: :Odysseas-Kimon
    type: :Man
  AssignClass (c303bc50-964f-4db0-bf07-fdc9b2bc18d9)
 Call ID: c303bc50-964f-4db0-bf07-fdc9b2bc18d9
  Args:
    source: :Aristides-Stavros
    type: :Man
  Finish (2ccc2ced-c5bc-4d28-bbfa-3a77af29f5b5)
 Call ID: 2ccc2ced-c5bc-4d28-bbfa-3a77af29f5b5
  Args: