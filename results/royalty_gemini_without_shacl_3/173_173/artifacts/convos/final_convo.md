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
Princess Irene of Greece and Denmark (Greek: Ειρήνη, romanized: Iríni; 11 May 1942 – 15 January 2026) was the youngest child and second daughter of King Paul of Greece and his wife, Queen Frederica.
She was the younger sister of Queen Sofía of Spain and King Constantine II of Greece.
From 1981 until her death, Irene lived permanently in Spain, becoming a part of the wider Spanish royal family as Queen Sofía's sister, to whose family she remained very close.
Early life

Irene was born on 11 May 1942 in Cape Town, Union of South Africa, where her parents were living in exile because of the German invasion of Greece during the Second World War.
She was the younger daughter of Paul, Crown Prince of Greece (later King Paul), and his wife Frederica of Hanover.
She was christened three weeks after her birth at her parents' Claremont rented home by the Metropolitan of the Holy Archdiocese of Johannesburg and Pretoria and was named after her paternal aunt Princess Irene, Duchess of Aosta.
She had ten godparents, including General Jan Smuts, Lady Katherine Brandram (her paternal aunt), King George II of Greece (her paternal uncle), Queen Mary of the United Kingdom, and the Duchess of Kent (her paternal first cousin once removed).
In 1944 the family moved to Egypt and returned to Greece in 1946 after the approval of the continuity of the Greek monarchy in the referendum with her uncle George II.
Irene was educated at Arsakion school at Psykhikó Palace in Greece and at Schule Schloss Salem in Baden-Württemberg, Germany.
Irene took up the piano in 1962.
As a young woman, Irene was courted by Prince Michel, Count of Évreux, younger son of the Orléanist pretender Henri, Count of Paris, until he met and later married a French noblewoman without his father's consent in 1967.
She was also rumoured to be a potential bride of Crown Prince Harald of Norway (later King Harald V) who later married Sonja Haraldsen in 1968.
Irene was one of the bridesmaids at the wedding of Spanish Prince Juan Carlos and Princess Sofía in 1962.
Her brother Constantine became King in 1964 after the death of their father.
Between her father's death and the birth of her niece Princess Alexia, Irene was heiress presumptive to the Greek throne.
Exile and later life

After her brother was dethroned in the Colonels' coup of 21 April 1967, Irene and the Royal Family moved to Italy after Constantine's unsuccessful countercoup against the junta.
With her mother Irene resided in Rome.
As Mahadevan grew frailer, he dictated his memoirs to Irene.
After her mother's death in 1981, she lived in Spain in an apartment at the Palace of Zarzuela in Madrid, the residence of her sister and brother-in-law, Queen Sofía and King Juan Carlos.
In the 1980s, during the BSE outbreak, Irene arranged for thousands of surplus cows from Europe and the United States to be shipped to India where they evaded slaughter.
During the 1981 Spanish coup attempt, Irene was at the Palace of Zarzuela with King Juan Carlos and her sister Queen Sofia; years later, she recounted the fear they both experienced when remembering the coup in Greece years earlier.
Irene accompanied Sofia in her official duties albeit discreetly.
In 2007, her biography Irene of Greece, the Rebel Princess was published.
On 16 March 2018, Irene obtained Spanish nationality and renounced her Greek nationality.
Personal life

Irene never married and had a passion for piano and archaeology.
With Sofía, they excavated the sites of the ancient village of Decelea and both, together with archaeologist Theophanó A. Arvanitopoulou, wrote two essays.
In 2000, Irene donated a selection of rare books and archaeological artefacts from the family collection to the Benaki Museum.
After the death of her father Paul, Irene became vegetarian.
In November 2023 it was made public that Irene was suffering from cognitive impairment.
Irene's last public appearance was at the wedding of her nephew and godson Prince Nikolaos in February 2025 in Athens.
In the summer of that year, her illness worsened, so she withdrew from public activities in which she accompanied her sister Queen Sofia, who adapted her schedule to Irene's condition.
On 13 January 2026, the Spanish Royal Household announced her condition had worsened and Queen Sofía cancelled all her public engagements to be at her side.
She died at the Palace of Zarzuela in Madrid, Spain, on 15 January, at the age of 83.
After private services at the Palace of Zarzuela, Irene's body—escorted by the Royal Guard—was laid in repose at the Cathedral of St Andrew and St Demetrius in Madrid on 17 January.



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
  AssignClass (8e0400d1-3a0d-478e-af72-190ac5ff00ba)
 Call ID: 8e0400d1-3a0d-478e-af72-190ac5ff00ba
  Args:
    type: :Woman
    source: Irene_of_Greece_and_Denmark
  AssignClass (782acbc8-3f3a-4e3d-8d17-47754ed18135)
 Call ID: 782acbc8-3f3a-4e3d-8d17-47754ed18135
  Args:
    type: :Person
    source: Irene_of_Greece_and_Denmark
  AddLiteral (36b6eac7-6a3b-472d-8a98-caa93bdac380)
 Call ID: 36b6eac7-6a3b-472d-8a98-caa93bdac380
  Args:
    source: Irene_of_Greece_and_Denmark
    literal_value: 1942
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (6feef52a-2ac5-46c1-a5df-0411a93b2983)
 Call ID: 6feef52a-2ac5-46c1-a5df-0411a93b2983
  Args:
    literal_value: 2026
    source: Irene_of_Greece_and_Denmark
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (bc1cad0e-300e-4612-ba1e-635b690cb934)
 Call ID: bc1cad0e-300e-4612-ba1e-635b690cb934
  Args:
    source: Paul_of_Greece
    type: :Man
  AssignClass (2fb8e540-bf21-4636-95d9-709629331b21)
 Call ID: 2fb8e540-bf21-4636-95d9-709629331b21
  Args:
    source: Paul_of_Greece
    type: :Person
  AssignClass (3e3ec84a-60b2-409d-b9a6-35243e7a1f87)
 Call ID: 3e3ec84a-60b2-409d-b9a6-35243e7a1f87
  Args:
    source: Frederica_of_Hanover
    type: :Woman
  AssignClass (e806fef3-43f8-49b4-9d22-125d416cb15f)
 Call ID: e806fef3-43f8-49b4-9d22-125d416cb15f
  Args:
    source: Frederica_of_Hanover
    type: :Person
  AddTriple (2bc546c4-cc87-4d8d-8c66-79752d8840b4)
 Call ID: 2bc546c4-cc87-4d8d-8c66-79752d8840b4
  Args:
    target: Paul_of_Greece
    relation: :hasFather
    source: Irene_of_Greece_and_Denmark
  AddTriple (178d1c94-cf78-4231-a1d1-bfa1892c188c)
 Call ID: 178d1c94-cf78-4231-a1d1-bfa1892c188c
  Args:
    relation: :hasMother
    target: Frederica_of_Hanover
    source: Irene_of_Greece_and_Denmark
  AssignClass (03febe21-dd79-4d9e-bbeb-845fc390636f)
 Call ID: 03febe21-dd79-4d9e-bbeb-845fc390636f
  Args:
    source: Sofia_of_Spain
    type: :Woman
  AssignClass (2631442d-8f7f-4e79-8220-ce29047a065a)
 Call ID: 2631442d-8f7f-4e79-8220-ce29047a065a
  Args:
    source: Sofia_of_Spain
    type: :Person
  AssignClass (dac0fcce-9822-4ddb-9e7c-46fa14c4658c)
 Call ID: dac0fcce-9822-4ddb-9e7c-46fa14c4658c
  Args:
    type: :Man
    source: Constantine_II_of_Greece
  AssignClass (a5c1bc80-409c-4da3-98dc-e8c081939011)
 Call ID: a5c1bc80-409c-4da3-98dc-e8c081939011
  Args:
    source: Constantine_II_of_Greece
    type: :Person
  AddTriple (8c8c3cc3-48be-4094-832e-89bd885a88b4)
 Call ID: 8c8c3cc3-48be-4094-832e-89bd885a88b4
  Args:
    relation: :isSisterOf
    target: Sofia_of_Spain
    source: Irene_of_Greece_and_Denmark
  AddTriple (64041ae6-fa04-40c6-a5a1-a6174c633b84)
 Call ID: 64041ae6-fa04-40c6-a5a1-a6174c633b84
  Args:
    relation: :isSisterOf
    target: Irene_of_Greece_and_Denmark
    source: Sofia_of_Spain
  AddTriple (3dc09942-5234-48ad-beb0-dd760c0dc3ca)
 Call ID: 3dc09942-5234-48ad-beb0-dd760c0dc3ca
  Args:
    source: Constantine_II_of_Greece
    relation: :isBrotherOf
    target: Irene_of_Greece_and_Denmark
  AddTriple (5520fdd2-2989-4a98-abac-b3ad48fd3683)
 Call ID: 5520fdd2-2989-4a98-abac-b3ad48fd3683
  Args:
    relation: :hasSister
    target: Sofia_of_Spain
    source: Irene_of_Greece_and_Denmark
  AddTriple (94f44e20-000a-4013-987e-2e1c283a9eac)
 Call ID: 94f44e20-000a-4013-987e-2e1c283a9eac
  Args:
    source: Irene_of_Greece_and_Denmark
    target: Constantine_II_of_Greece
    relation: :hasBrother
  AssignClass (3cfb0284-2f0a-4419-a3fd-71b7fe85de4b)
 Call ID: 3cfb0284-2f0a-4419-a3fd-71b7fe85de4b
  Args:
    type: :Man
    source: Juan_Carlos_of_Spain
  AssignClass (623194d2-acde-4302-9c13-5b9f5e095f2e)
 Call ID: 623194d2-acde-4302-9c13-5b9f5e095f2e
  Args:
    type: :Person
    source: Juan_Carlos_of_Spain
  AssignClass (0df6639d-ee84-4f99-a51c-bb5d2fa634e0)
 Call ID: 0df6639d-ee84-4f99-a51c-bb5d2fa634e0
  Args:
    source: Alexia_of_Greece
    type: :Woman
  AssignClass (eea87e79-8b1d-47f2-8f7c-5a53450a0c57)
 Call ID: eea87e79-8b1d-47f2-8f7c-5a53450a0c57
  Args:
    source: Alexia_of_Greece
    type: :Person
  AddTriple (c7053071-fefd-49df-9192-b21c345c35ff)
 Call ID: c7053071-fefd-49df-9192-b21c345c35ff
  Args:
    target: Alexia_of_Greece
    relation: :isParentOf
    source: Constantine_II_of_Greece
  AssignClass (f16831d8-22dd-4895-84b4-a5619e1391e0)
 Call ID: f16831d8-22dd-4895-84b4-a5619e1391e0
  Args:
    type: :Man
    source: Nikolaos_of_Greece
  AssignClass (3c85b8e1-6934-49fa-b64a-bdf3e58fd312)
 Call ID: 3c85b8e1-6934-49fa-b64a-bdf3e58fd312
  Args:
    source: Nikolaos_of_Greece
    type: :Person
  Finish (e63e4191-1cc9-4cc3-ba30-e0a58d11d8f8)
 Call ID: e63e4191-1cc9-4cc3-ba30-e0a58d11d8f8
  Args: