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
The Duke of CalabriaThe Duchess of Calabria


Prince Jaime of Bourbon-Two Sicilies, Duke of Noto (born 26 June 1993) is a Spanish aristocrat and heir to the headship of the House of Bourbon-Two Sicilies as eldest son of Prince Pedro, Duke of Calabria.
Biography

Jaime was born on 26 June 1993 in Madrid, Spain, as the illegitimate son of Prince Pedro, then Duke of Noto (born 16 October 1968), and Sofia Landaluce y Melgarejo (born 23 November 1973).
His paternal grandparents are Infante Carlos, Duke of Calabria (1938–2015), and his wife, Princess Anne of Orléans.
The Duke of Noto was educated at the Centro Universitario Villanueva (with a degree in law) and then obtained a master's degree in management from the IE University Business School.
Claim to the throne

Jaime's grandfather, Infante Don Carlos of Spain, Duke of Calabria, had to consider whether the future marriage of Prince Pedro to Sofía Landaluce y Melgarejo would meet the conditions established in the Sovereign Act that was signed in Naples on 7 April 1829, Law no. 2362, which gave the "head of Our House of Bourbon... such authority as is necessary to protect the purity and splendour of the throne", by requiring all members of the dynasty to have formal permission to marry.
The marriages of all members of the dynasty that had been considered capable of transmitting dynastic rights had been to royal princesses until the marriage of Prince Ranieri to Countess Carolina Zamoyska in 1929.
The ultimate decision of Infante Carlos to permit his son's marriage to be considered dynastic followed the marriages of the daughters of King Juan Carlos without them being required to renounce their right of succession to the Spanish throne, and a change in the marriage rules of the House of Austria.
Infante Carlos and his wife attended the marriage of Prince Pedro on 30 March 2001, and the marriage is treated as a dynastic marriage transmitting full rights of succession to all the children of Prince Pedro and his wife.
It was made clear by the date of the marriage of the future King Felipe VI in 2004 that the children of Prince Pedro and his wife had full dynastic rights, and the children bear the style of Royal Highness and the title of Prince(ss) of Bourbon-Two Sicilies.
Marriage and issue

On 25 September 2021 at Monreale Cathedral in Palermo, Jaime married Lady Charlotte Lindesay-Bethune, youngest daughter of James Lindesay-Bethune, 16th Earl of Lindsay, and his wife, Diana Mary Chamberlayne-Macdonald.
On 13 October 2023, the Duke and Duchess of Noto had their first child in London – a daughter named Francesca Sofía.
On 19 November 2025, the Duke and Duchess of Noto had their second child in London – a daughter named Ines.



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
  AssignClass (333a8c35-d22e-4137-b40a-4553331f8906)
 Call ID: 333a8c35-d22e-4137-b40a-4553331f8906
  Args:
    type: :Man
    source: PrinceJaimeOfBourbonTwoSicilies
  AssignClass (85657567-2067-47da-aab1-ed9eaf024b6c)
 Call ID: 85657567-2067-47da-aab1-ed9eaf024b6c
  Args:
    type: :Person
    source: PrinceJaimeOfBourbonTwoSicilies
  AddLiteral (f7aa7e15-6428-4221-927c-307275e13ac5)
 Call ID: f7aa7e15-6428-4221-927c-307275e13ac5
  Args:
    literal_value: 1993
    literal_type: xsd:integer
    source: PrinceJaimeOfBourbonTwoSicilies
    relation: :hasBirthYear
  AssignClass (301b4bce-bb3b-422c-bd60-1f483c5503c7)
 Call ID: 301b4bce-bb3b-422c-bd60-1f483c5503c7
  Args:
    type: :Man
    source: PrincePedroDukeOfCalabria
  AssignClass (5eebcbce-7d85-4a91-8041-74fb2a827615)
 Call ID: 5eebcbce-7d85-4a91-8041-74fb2a827615
  Args:
    type: :Person
    source: PrincePedroDukeOfCalabria
  AddLiteral (0a6ecd24-7465-4450-976a-69d14c23e97d)
 Call ID: 0a6ecd24-7465-4450-976a-69d14c23e97d
  Args:
    source: PrincePedroDukeOfCalabria
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1968
  AssignClass (c9edd744-4f8e-4195-8bb4-2fe20146d9e6)
 Call ID: c9edd744-4f8e-4195-8bb4-2fe20146d9e6
  Args:
    type: :Woman
    source: SofiaLandaluceYMelgarejo
  AssignClass (1e4cbb61-6aae-4cd3-b9ba-d948a78529ef)
 Call ID: 1e4cbb61-6aae-4cd3-b9ba-d948a78529ef
  Args:
    type: :Person
    source: SofiaLandaluceYMelgarejo
  AddLiteral (385191ba-9b46-4193-892e-e8c201f6a90a)
 Call ID: 385191ba-9b46-4193-892e-e8c201f6a90a
  Args:
    literal_value: 1973
    literal_type: xsd:integer
    source: SofiaLandaluceYMelgarejo
    relation: :hasBirthYear
  AddTriple (d1194d35-0b0c-4f32-bbb5-cd32fc7fbcca)
 Call ID: d1194d35-0b0c-4f32-bbb5-cd32fc7fbcca
  Args:
    target: PrincePedroDukeOfCalabria
    source: PrinceJaimeOfBourbonTwoSicilies
    relation: :isSonOf
  AddTriple (6af32858-4e39-457e-97f1-fb6a2321e71a)
 Call ID: 6af32858-4e39-457e-97f1-fb6a2321e71a
  Args:
    source: PrinceJaimeOfBourbonTwoSicilies
    relation: :isSonOf
    target: SofiaLandaluceYMelgarejo
  AssignClass (4753e84c-f2f7-4170-9afc-6f88b9cf75bb)
 Call ID: 4753e84c-f2f7-4170-9afc-6f88b9cf75bb
  Args:
    type: :Man
    source: InfanteCarlosDukeOfCalabria
  AssignClass (242591cd-9710-44a6-9c14-bce97f4ef386)
 Call ID: 242591cd-9710-44a6-9c14-bce97f4ef386
  Args:
    type: :Person
    source: InfanteCarlosDukeOfCalabria
  AddLiteral (8a3c7068-2f66-4398-a4ba-29e249c673a5)
 Call ID: 8a3c7068-2f66-4398-a4ba-29e249c673a5
  Args:
    relation: :hasBirthYear
    source: InfanteCarlosDukeOfCalabria
    literal_type: xsd:integer
    literal_value: 1938
  AddLiteral (97269230-c21c-49de-a228-57e33f671313)
 Call ID: 97269230-c21c-49de-a228-57e33f671313
  Args:
    relation: :hasDeathYear
    source: InfanteCarlosDukeOfCalabria
    literal_type: xsd:integer
    literal_value: 2015
  AssignClass (1442d23b-fc89-4367-9e97-4c06e12249fd)
 Call ID: 1442d23b-fc89-4367-9e97-4c06e12249fd
  Args:
    type: :Woman
    source: PrincessAnneOfOrleans
  AssignClass (d1d8f828-6381-4a16-86c5-22beecddd90b)
 Call ID: d1d8f828-6381-4a16-86c5-22beecddd90b
  Args:
    type: :Person
    source: PrincessAnneOfOrleans
  AddTriple (af76e119-c4b7-40df-9f6d-6efb3ac292c5)
 Call ID: af76e119-c4b7-40df-9f6d-6efb3ac292c5
  Args:
    source: InfanteCarlosDukeOfCalabria
    relation: :isFatherOf
    target: PrincePedroDukeOfCalabria
  AddTriple (d4665bbe-32ce-4ece-84ab-d8fbef5b204a)
 Call ID: d4665bbe-32ce-4ece-84ab-d8fbef5b204a
  Args:
    target: PrincePedroDukeOfCalabria
    source: PrincessAnneOfOrleans
    relation: :isMotherOf
  AssignClass (da017e87-0166-47e0-91bb-3afcf47edc4e)
 Call ID: da017e87-0166-47e0-91bb-3afcf47edc4e
  Args:
    type: :Woman
    source: LadyCharlotteLindesayBethune
  AssignClass (402f44a8-1ace-4358-b97d-39defed71140)
 Call ID: 402f44a8-1ace-4358-b97d-39defed71140
  Args:
    type: :Person
    source: LadyCharlotteLindesayBethune
  AddTriple (ae4e267d-e230-4284-bfcd-046563756ea2)
 Call ID: ae4e267d-e230-4284-bfcd-046563756ea2
  Args:
    target: LadyCharlotteLindesayBethune
    relation: :hasRelation
    source: PrinceJaimeOfBourbonTwoSicilies
  AssignClass (50e313aa-6cfe-416b-8a90-b5b69bdd7cae)
 Call ID: 50e313aa-6cfe-416b-8a90-b5b69bdd7cae
  Args:
    type: :Man
    source: JamesLindesayBethune16thEarlOfLindsay
  AssignClass (4695dd46-4efb-44f4-81f7-62eae2fe71a8)
 Call ID: 4695dd46-4efb-44f4-81f7-62eae2fe71a8
  Args:
    type: :Person
    source: JamesLindesayBethune16thEarlOfLindsay
  AssignClass (8c94051b-4e8f-4beb-b74f-dcf47632b02e)
 Call ID: 8c94051b-4e8f-4beb-b74f-dcf47632b02e
  Args:
    type: :Woman
    source: DianaMaryChamberlayneMacdonald
  AssignClass (bf138e34-ab8e-465f-97cc-afd98660e7ae)
 Call ID: bf138e34-ab8e-465f-97cc-afd98660e7ae
  Args:
    type: :Person
    source: DianaMaryChamberlayneMacdonald
  AddTriple (6842e04a-ee3a-4f85-a562-fecaa464f47e)
 Call ID: 6842e04a-ee3a-4f85-a562-fecaa464f47e
  Args:
    relation: :isDaughterOf
    source: LadyCharlotteLindesayBethune
    target: JamesLindesayBethune16thEarlOfLindsay
  AddTriple (aa48e437-28a1-4d46-9110-82226ef4fee4)
 Call ID: aa48e437-28a1-4d46-9110-82226ef4fee4
  Args:
    target: DianaMaryChamberlayneMacdonald
    source: LadyCharlotteLindesayBethune
    relation: :isDaughterOf
  AssignClass (1f56d8e2-6180-4c20-bb5f-4c688615b0bd)
 Call ID: 1f56d8e2-6180-4c20-bb5f-4c688615b0bd
  Args:
    type: :Woman
    source: FrancescaSofia
  AssignClass (53ec723b-417d-410d-bd3d-8b6c6be9dd65)
 Call ID: 53ec723b-417d-410d-bd3d-8b6c6be9dd65
  Args:
    type: :Person
    source: FrancescaSofia
  AddTriple (6913a156-9d03-41de-aa74-43047023b0b4)
 Call ID: 6913a156-9d03-41de-aa74-43047023b0b4
  Args:
    target: PrinceJaimeOfBourbonTwoSicilies
    source: FrancescaSofia
    relation: :isDaughterOf
  AddTriple (830cc9d1-d5d9-4d8a-ac0f-206e9ad6fc90)
 Call ID: 830cc9d1-d5d9-4d8a-ac0f-206e9ad6fc90
  Args:
    relation: :isDaughterOf
    source: FrancescaSofia
    target: LadyCharlotteLindesayBethune
  AssignClass (defa50e2-8490-47ac-be22-45a925693d8b)
 Call ID: defa50e2-8490-47ac-be22-45a925693d8b
  Args:
    type: :Woman
    source: Ines
  AssignClass (29827a2d-7991-447d-8fa2-0261e509f480)
 Call ID: 29827a2d-7991-447d-8fa2-0261e509f480
  Args:
    type: :Person
    source: Ines
  AddTriple (ba665354-5487-4144-aa6a-c51fb7cfad6d)
 Call ID: ba665354-5487-4144-aa6a-c51fb7cfad6d
  Args:
    relation: :isDaughterOf
    source: Ines
    target: PrinceJaimeOfBourbonTwoSicilies
  AddTriple (95f4a569-8be3-4b29-87a3-78d09c8848c5)
 Call ID: 95f4a569-8be3-4b29-87a3-78d09c8848c5
  Args:
    target: LadyCharlotteLindesayBethune
    source: Ines
    relation: :isDaughterOf
  Finish (e307d1b7-ce47-4d69-a2c3-914d15aacae2)
 Call ID: e307d1b7-ce47-4d69-a2c3-914d15aacae2
  Args: