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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Alexander Karageorgevitch (Serbian Cyrillic: Александар Карађорђевић, romanized: Aleksandar Karađorđević; born 15 January 1982), also known as Prince Alexander of Serbia and Yugoslavia or Prince Aleksandar III Karađorđević, is a member of the House of Karađorđević, the former ruling family of the defunct Kingdom of Yugoslavia.
Early life and education

Prince Alexander was born 15 January 1982 in Vienna, Virginia, Alexander is the third and youngest child of the last crown prince of Yugoslavia, Alexander, and his first wife, Princess Maria da Gloria of Orléans-Braganza.
His godparents are Queen Sofía of Spain, King Constantine II of Greece (first cousins of his father), and Princess Anne, Duchess of Calabria (first cousin of his mother).
Alexander lived in Virginia until 1984.
In 1982, Alexander and his twin brother were baptized by Lavrentije, Serbian Orthodox Bishop of Western Europe, at a castle in Villamanrique de la Condesa, near Seville, Spain.
Alexander's parents divorced in 1985.
After the divorce, his father married Katherine Clairy Batis later that year, while his mother married Ignacio, 19th Duke of Segorbe in the same year.
Through his mother, Alexander has two younger half-sisters, Sol María de la Blanca Medina y Orléans-Braganza, 54th Countess of Ampurias (b. 1986) and Ana Luna Medina y Orléans-Braganza, 17th Countess of Ricla (b. 1988).
Alexander was educated in London and Canterbury with his twin brother.
Alexander was at a graduate school at an American university completing a MFA degree in advertising (Art Direction).
Patronages

In Serbia he is Chairman of the Board of Directors of the Crown Prince Foundation for Education and Culture (since 2024).
Personal life

Prince Alexander attended the reburial of his grandparents King Peter II and Queen Alexandra, great-grandmother Queen Maria, and granduncle Prince Andrew in the Royal Family Mausoleum at Oplenac on 26 May 2013.
The Serbian Royal Regalia were placed over King Peter's coffin, having Alexander placing a diamond sabre near to the Karađorđević Crown.
In 2015, Alexander dated Dunja Kusturica, a daughter of Serbian filmmaker and musician Emir Kusturica.
At the time, their relationship was compared to one of Catherine and Prince William by Serbian media.
On 17 July 2015, Prince Alexander and his brothers were present at their father's 70th birthday celebration in Belgrade.
Ancestors

Alexander is a member of the House of Karađorđević.
Through his father, Alexander descends from kings Nicholas I of Montenegro, Ferdinand I of Romania, and Alexander of Greece, and furthermore from emperors Nicholas I of Russia and Frederick III of the Germans and Queen Victoria of the United Kingdom of Great Britain and Ireland.
Through his mother, Alexander descends from the Emperor Pedro II of Brazil, and kings Louis Philippe I of France and Francis I of the Two Sicilies, and furthermore from Francis I, Holy Roman Emperor and king Charles III of Spain.



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
  AssignClass (e8a9c3b8-307a-45c1-9e15-06f91d928bca)
 Call ID: e8a9c3b8-307a-45c1-9e15-06f91d928bca
  Args:
    source: :AlexanderKarageorgevitch
    type: :Man
  AssignClass (11fd8502-9528-4f3c-b1f7-bcdcc2f0b857)
 Call ID: 11fd8502-9528-4f3c-b1f7-bcdcc2f0b857
  Args:
    source: :AlexanderKarageorgevitch
    type: :Person
  AddLiteral (bcb7a8a4-5148-4b24-ae69-48d3c6d72f6c)
 Call ID: bcb7a8a4-5148-4b24-ae69-48d3c6d72f6c
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :AlexanderKarageorgevitch
    literal_value: 1982
  AddLiteral (64ded986-3239-45b9-a450-1c66a8ff707e)
 Call ID: 64ded986-3239-45b9-a450-1c66a8ff707e
  Args:
    literal_type: xsd:string
    relation: :knownAs
    source: :AlexanderKarageorgevitch
    literal_value: Prince Alexander of Serbia and Yugoslavia
  AddLiteral (ba5aa2ae-58b8-4147-9865-9cac881e7cd7)
 Call ID: ba5aa2ae-58b8-4147-9865-9cac881e7cd7
  Args:
    literal_value: Prince Aleksandar III Karađorđević
    literal_type: xsd:string
    relation: :knownAs
    source: :AlexanderKarageorgevitch
  AssignClass (50c704ca-aa8e-40f1-ad5d-22120c1d154e)
 Call ID: 50c704ca-aa8e-40f1-ad5d-22120c1d154e
  Args:
    type: :Man
    source: :AlexanderSr
  AssignClass (5c6b1796-43f8-497b-bfad-66c40ce32250)
 Call ID: 5c6b1796-43f8-497b-bfad-66c40ce32250
  Args:
    source: :AlexanderSr
    type: :Ancestor
  AssignClass (be926e0f-7111-431b-b7c0-f1b8f7051250)
 Call ID: be926e0f-7111-431b-b7c0-f1b8f7051250
  Args:
    source: :AlexanderSr
    type: :Person
  AddTriple (82aed0d7-3228-42ec-ac72-d15cb0c96822)
 Call ID: 82aed0d7-3228-42ec-ac72-d15cb0c96822
  Args:
    source: :AlexanderKarageorgevitch
    relation: :hasFather
    target: :AlexanderSr
  AssignClass (06c9f81e-143f-402a-922e-27487953587a)
 Call ID: 06c9f81e-143f-402a-922e-27487953587a
  Args:
    source: :MariaDaGloria
    type: :Woman
  AssignClass (423c94f9-3ec2-44fe-9a9d-7921e77deb78)
 Call ID: 423c94f9-3ec2-44fe-9a9d-7921e77deb78
  Args:
    source: :MariaDaGloria
    type: :Ancestor
  AssignClass (8b948577-af95-4a3c-a818-ffea0697b422)
 Call ID: 8b948577-af95-4a3c-a818-ffea0697b422
  Args:
    type: :Person
    source: :MariaDaGloria
  AddTriple (f6e6cda6-21de-4c66-87fb-62902a516c80)
 Call ID: f6e6cda6-21de-4c66-87fb-62902a516c80
  Args:
    target: :MariaDaGloria
    source: :AlexanderKarageorgevitch
    relation: :hasMother
  AssignClass (775b59db-05d0-49a3-a8a4-6647dc319100)
 Call ID: 775b59db-05d0-49a3-a8a4-6647dc319100
  Args:
    source: :KatherineClairyBatis
    type: :Woman
  AssignClass (23a54a36-c6f0-4b93-b9da-657155872166)
 Call ID: 23a54a36-c6f0-4b93-b9da-657155872166
  Args:
    source: :KatherineClairyBatis
    type: :Person
  AssignClass (46781f38-4a5d-4d95-8447-9970070f7a93)
 Call ID: 46781f38-4a5d-4d95-8447-9970070f7a93
  Args:
    source: :IgnacioDukeOfSegorbe
    type: :Man
  AssignClass (a741a933-fb07-4094-bcb2-e348b956feab)
 Call ID: a741a933-fb07-4094-bcb2-e348b956feab
  Args:
    source: :IgnacioDukeOfSegorbe
    type: :Person
  AssignClass (85f6c426-60bf-4665-b112-8e8004eebce5)
 Call ID: 85f6c426-60bf-4665-b112-8e8004eebce5
  Args:
    type: :Woman
    source: :SolMariaMedina
  AssignClass (d6f7b913-a994-47b2-b039-f7aa9e9eab8c)
 Call ID: d6f7b913-a994-47b2-b039-f7aa9e9eab8c
  Args:
    source: :SolMariaMedina
    type: :Person
  AddTriple (a89ffdc4-4d10-4b19-8bc4-0f9adc5fc7fd)
 Call ID: a89ffdc4-4d10-4b19-8bc4-0f9adc5fc7fd
  Args:
    target: :MariaDaGloria
    source: :SolMariaMedina
    relation: :hasMother
  AssignClass (e2451604-244c-4f1c-9c9f-50e6fa05b622)
 Call ID: e2451604-244c-4f1c-9c9f-50e6fa05b622
  Args:
    source: :AnaLunaMedina
    type: :Woman
  AssignClass (7688a3fb-0757-4a16-ba97-0ab0b006e4d9)
 Call ID: 7688a3fb-0757-4a16-ba97-0ab0b006e4d9
  Args:
    type: :Person
    source: :AnaLunaMedina
  AddTriple (11091724-be3d-443e-8dce-bfaa7c14a106)
 Call ID: 11091724-be3d-443e-8dce-bfaa7c14a106
  Args:
    target: :MariaDaGloria
    source: :AnaLunaMedina
    relation: :hasMother
  AssignClass (a3cfe97a-4d35-4fcc-9097-0c731b1c3dad)
 Call ID: a3cfe97a-4d35-4fcc-9097-0c731b1c3dad
  Args:
    source: :PeterII
    type: :Man
  AssignClass (799f90f4-206a-4b0e-b05b-f9ebb8b764e3)
 Call ID: 799f90f4-206a-4b0e-b05b-f9ebb8b764e3
  Args:
    source: :PeterII
    type: :Ancestor
  AssignClass (7f283204-a7f1-43c7-9f0b-633b333b989b)
 Call ID: 7f283204-a7f1-43c7-9f0b-633b333b989b
  Args:
    type: :Person
    source: :PeterII
  AssignClass (a359fa9e-a9e3-4c5a-ac7d-623d36ed5263)
 Call ID: a359fa9e-a9e3-4c5a-ac7d-623d36ed5263
  Args:
    source: :QueenAlexandra
    type: :Woman
  AssignClass (175cee4b-3764-4bed-9d83-0baae74ff157)
 Call ID: 175cee4b-3764-4bed-9d83-0baae74ff157
  Args:
    type: :Ancestor
    source: :QueenAlexandra
  AssignClass (d04257b1-b0f7-4133-b941-078d94641010)
 Call ID: d04257b1-b0f7-4133-b941-078d94641010
  Args:
    type: :Person
    source: :QueenAlexandra
  AssignClass (7dfac40f-ea79-4e07-aedb-f27ce6d265d1)
 Call ID: 7dfac40f-ea79-4e07-aedb-f27ce6d265d1
  Args:
    source: :QueenMaria
    type: :Woman
  AssignClass (f5113d9b-1058-49b7-9c0b-35f134f34885)
 Call ID: f5113d9b-1058-49b7-9c0b-35f134f34885
  Args:
    source: :QueenMaria
    type: :Ancestor
  AssignClass (82282729-1ff0-49db-a297-ddb7acd3927e)
 Call ID: 82282729-1ff0-49db-a297-ddb7acd3927e
  Args:
    type: :Person
    source: :QueenMaria
  AssignClass (d62f7ce0-ec08-40de-b1fc-ad757dba5595)
 Call ID: d62f7ce0-ec08-40de-b1fc-ad757dba5595
  Args:
    source: :PrinceAndrew
    type: :Man
  AssignClass (2675c353-059f-4b05-9a06-e198077c7187)
 Call ID: 2675c353-059f-4b05-9a06-e198077c7187
  Args:
    source: :PrinceAndrew
    type: :Ancestor
  AssignClass (5ee4343f-f041-4a57-b581-62e4dae09bba)
 Call ID: 5ee4343f-f041-4a57-b581-62e4dae09bba
  Args:
    source: :PrinceAndrew
    type: :Person
  Finish (ed418122-2bfc-4740-b0f5-5ed074dcb506)
 Call ID: ed418122-2bfc-4740-b0f5-5ed074dcb506
  Args: