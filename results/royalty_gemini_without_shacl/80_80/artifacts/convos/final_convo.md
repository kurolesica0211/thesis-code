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
The Duchess of Montpensier


The Count of ÉvreuxThe Countess of Évreux


Princess Béatrice


The Duke of OrléansThe Duchess of Orléans


The Dowager Countess of La Marche


The Countess of Schönborn-Buchheim


Princess Hélène, Countess of Limburg Stirum


The Dowager Duchess of Calabria


The Dowager Duchess of Württemberg


Princess Claude, Mrs. Gandolfi


Princess Chantal, Baroness of Sambucy de Sorgue


Princess Claude of Orléans (Claude Marie Agnès Catherine; born 11 December 1943) is a French princess of the House of Orléans.
Biography

Family

Claude was born on 11 December 1943 in Larache, Morocco as the ninth child and fifth daughter of Henri, Count of Paris, Orléanist claimant to the French throne, and Princess Isabelle of Orléans-Braganza.
One of eleven siblings, Claude's eldest brother was Henri, Count of Paris, who succeeded their father as head of the Orléans family, and two of her sisters also became consorts of pretenders to abolished thrones; Anne, Duchess of Calabria and Diane, Duchess of Württemberg.
Marriage and issue

On 22 July 1964 in Sintra, Princess Claude married her second cousin, Prince Amedeo of Savoy, Duke of Aosta.
He was the only son of Prince Aimone, Duke of Aosta, second cousin once removed of Italy's last king, Umberto II.
Aimone was briefly made nominal head of an Italian puppet state during World War II as King Tomislav II of Croatia.
Claude was the third Orleanist princess to hold the title Duchess of Aosta by marriage.
The couple met while attending the wedding of Infante Juan Carlos of Spain and Princess Sophia of Greece and Denmark in May 1962 in Athens.
A Savoy family council having met at King Umberto's residence in exile at Cimiez, France, in the summer of 1963, another was held in London secretly at the king's hospital bedside to discuss the prospect of the king's only son Vittorio Emanuele, Prince of Naples, choosing to marry a commoner, Marina Doria, which had become the subject of much media speculation.
In view of his illness, Amedeo's imminent marriage to a suitable princess, and his son's ongoing relationship with Doria, Umberto contemplated publicly abdicating (having left Italy for exile in 1946 pursuant to an anti-monarchy plebiscite, he had not formally renounced) and recognizing Amedeo as the successor to his claim to Italy's abolished throne.
The wedding was attended by 300 guests, including King Umberto and the Prince and Princess of Spain.
After the duke completed his duties as a naval officer, the couple were given the Borro by Aimone's mother, a large estate in the Tuscan village of San Giustino Valdarno, near Fiesole, Italy, where they cultivated vineyards.
Amedeo was remarried later that year to Silvia Paternò di Spedalotto, while Claude remarried twice: civilly on 27 April 1982 in Port-au-Prince, Haiti with Luigi Arnaldo La Cagnina (divorced in 1996), a television journalist in the United States and Canada, and both civilly and religiously with Enrico Gandolfi in 2006 in Oreno, Milan.



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
  AssignClass (98a4d935-5496-400e-af51-243a692d9b89)
 Call ID: 98a4d935-5496-400e-af51-243a692d9b89
  Args:
    source: :Claude_of_Orleans
    type: :Person
  AssignClass (9e83f237-e182-4800-bd64-69f2ce0c16a3)
 Call ID: 9e83f237-e182-4800-bd64-69f2ce0c16a3
  Args:
    type: :Woman
    source: :Claude_of_Orleans
  AddLiteral (9415952b-a408-4d2e-99d1-c0fe869f42bd)
 Call ID: 9415952b-a408-4d2e-99d1-c0fe869f42bd
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Claude_of_Orleans
    literal_value: 1943
  AssignClass (3af4db6a-4931-4a2a-8990-645eb0fbd593)
 Call ID: 3af4db6a-4931-4a2a-8990-645eb0fbd593
  Args:
    source: :Henri_Count_of_Paris
    type: :Person
  AssignClass (6d5164be-9ce2-4a58-bd30-988c6d204a54)
 Call ID: 6d5164be-9ce2-4a58-bd30-988c6d204a54
  Args:
    type: :Man
    source: :Henri_Count_of_Paris
  AssignClass (1ac77549-9558-4802-a076-0cd61df893c0)
 Call ID: 1ac77549-9558-4802-a076-0cd61df893c0
  Args:
    source: :Henri_Count_of_Paris
    type: :Ancestor
  AssignClass (e700463a-7c3a-4c85-8d99-d5e295023b66)
 Call ID: e700463a-7c3a-4c85-8d99-d5e295023b66
  Args:
    source: :Isabelle_of_Orleans_Braganza
    type: :Person
  AssignClass (2df738fd-2e09-4c18-82a3-5cd184c79a04)
 Call ID: 2df738fd-2e09-4c18-82a3-5cd184c79a04
  Args:
    source: :Isabelle_of_Orleans_Braganza
    type: :Woman
  AssignClass (8c0f03ac-1b73-44bb-b85b-ced35030666f)
 Call ID: 8c0f03ac-1b73-44bb-b85b-ced35030666f
  Args:
    source: :Isabelle_of_Orleans_Braganza
    type: :Ancestor
  AddTriple (c059d0dd-57e4-48f7-807a-72104bb38d6a)
 Call ID: c059d0dd-57e4-48f7-807a-72104bb38d6a
  Args:
    target: :Henri_Count_of_Paris
    relation: :isChildOf
    source: :Claude_of_Orleans
  AddTriple (4c2dcc6d-6596-4ec2-a3b1-68d3d5ccb7c6)
 Call ID: 4c2dcc6d-6596-4ec2-a3b1-68d3d5ccb7c6
  Args:
    target: :Isabelle_of_Orleans_Braganza
    relation: :isChildOf
    source: :Claude_of_Orleans
  AssignClass (65b44fc1-4a55-4035-8a9a-3b996037e42b)
 Call ID: 65b44fc1-4a55-4035-8a9a-3b996037e42b
  Args:
    source: :Henri_Count_of_Paris_Jr
    type: :Person
  AssignClass (231eb42c-94df-47b9-8b1b-7e550db46f5e)
 Call ID: 231eb42c-94df-47b9-8b1b-7e550db46f5e
  Args:
    type: :Man
    source: :Henri_Count_of_Paris_Jr
  AddTriple (50721b32-feb4-42b6-b07a-f20625bd8fa8)
 Call ID: 50721b32-feb4-42b6-b07a-f20625bd8fa8
  Args:
    target: :Henri_Count_of_Paris_Jr
    relation: :isSiblingOf
    source: :Claude_of_Orleans
  AssignClass (4e01f81b-b097-4a6d-8a9e-6475be711676)
 Call ID: 4e01f81b-b097-4a6d-8a9e-6475be711676
  Args:
    source: :Anne_Duchess_of_Calabria
    type: :Person
  AssignClass (e8eda782-3ba8-40b5-99be-f95765e2025d)
 Call ID: e8eda782-3ba8-40b5-99be-f95765e2025d
  Args:
    source: :Anne_Duchess_of_Calabria
    type: :Woman
  AddTriple (c96f2bf0-534a-4fd9-b241-b3daa20d0821)
 Call ID: c96f2bf0-534a-4fd9-b241-b3daa20d0821
  Args:
    target: :Anne_Duchess_of_Calabria
    relation: :isSiblingOf
    source: :Claude_of_Orleans
  AssignClass (6fb1346d-3ba6-43d3-8927-cd008b3f06b2)
 Call ID: 6fb1346d-3ba6-43d3-8927-cd008b3f06b2
  Args:
    type: :Person
    source: :Diane_Duchess_of_Wurttemberg
  AssignClass (9e39603c-2222-4b55-873e-56c180e7b174)
 Call ID: 9e39603c-2222-4b55-873e-56c180e7b174
  Args:
    source: :Diane_Duchess_of_Wurttemberg
    type: :Woman
  AddTriple (866002c3-fe22-49bf-8404-15bb7e9e6fa6)
 Call ID: 866002c3-fe22-49bf-8404-15bb7e9e6fa6
  Args:
    source: :Claude_of_Orleans
    relation: :isSiblingOf
    target: :Diane_Duchess_of_Wurttemberg
  AssignClass (d0b98777-6d60-45d6-aac6-f6706cded689)
 Call ID: d0b98777-6d60-45d6-aac6-f6706cded689
  Args:
    source: :Amedeo_Duke_of_Aosta
    type: :Person
  AssignClass (d87584e2-72f4-45cb-bfe5-9b730003a056)
 Call ID: d87584e2-72f4-45cb-bfe5-9b730003a056
  Args:
    source: :Amedeo_Duke_of_Aosta
    type: :Man
  AssignClass (f910223b-27b5-4ed2-a02b-5b2c53912f93)
 Call ID: f910223b-27b5-4ed2-a02b-5b2c53912f93
  Args:
    type: :Person
    source: :Aimone_Duke_of_Aosta
  AssignClass (12016ebc-4378-4b6c-b9d0-72721f3f7612)
 Call ID: 12016ebc-4378-4b6c-b9d0-72721f3f7612
  Args:
    type: :Man
    source: :Aimone_Duke_of_Aosta
  AssignClass (60eeb10e-e75c-4e89-a14b-a1073ebfeb1b)
 Call ID: 60eeb10e-e75c-4e89-a14b-a1073ebfeb1b
  Args:
    type: :Ancestor
    source: :Aimone_Duke_of_Aosta
  AddTriple (5c396ba3-97b4-48e4-9b41-a9a90d5e83ac)
 Call ID: 5c396ba3-97b4-48e4-9b41-a9a90d5e83ac
  Args:
    source: :Amedeo_Duke_of_Aosta
    relation: :isChildOf
    target: :Aimone_Duke_of_Aosta
  AddLiteral (00a19556-74e6-4db0-9d23-e86b0f78d0e9)
 Call ID: 00a19556-74e6-4db0-9d23-e86b0f78d0e9
  Args:
    literal_type: xsd:integer
    literal_value: 1964
    relation: :hasMarriageYear
    source: :Claude_of_Orleans
  AddTriple (990d9e75-8e8b-4927-9792-b22137871d65)
 Call ID: 990d9e75-8e8b-4927-9792-b22137871d65
  Args:
    relation: :hasRelation
    source: :Claude_of_Orleans
    target: :Amedeo_Duke_of_Aosta
  AssignClass (2fb43e31-c911-4c62-baea-1e468d795551)
 Call ID: 2fb43e31-c911-4c62-baea-1e468d795551
  Args:
    source: :Luigi_Arnaldo_La_Cagnina
    type: :Person
  AssignClass (0ab93f63-9feb-4357-80e3-b8586f12ce5d)
 Call ID: 0ab93f63-9feb-4357-80e3-b8586f12ce5d
  Args:
    source: :Luigi_Arnaldo_La_Cagnina
    type: :Man
  AddTriple (2bada494-b8c3-435e-a8df-2fd3e4e0a258)
 Call ID: 2bada494-b8c3-435e-a8df-2fd3e4e0a258
  Args:
    relation: :hasRelation
    source: :Claude_of_Orleans
    target: :Luigi_Arnaldo_La_Cagnina
  AssignClass (39cc1f10-1dfb-4807-af8f-9f2e12fe75c3)
 Call ID: 39cc1f10-1dfb-4807-af8f-9f2e12fe75c3
  Args:
    source: :Enrico_Gandolfi
    type: :Person
  AssignClass (02c8f83c-aec0-477c-a3e5-c5122d4336e4)
 Call ID: 02c8f83c-aec0-477c-a3e5-c5122d4336e4
  Args:
    type: :Man
    source: :Enrico_Gandolfi
  AddTriple (228ee07f-d69c-4d7f-a8f8-9fe3c7429160)
 Call ID: 228ee07f-d69c-4d7f-a8f8-9fe3c7429160
  Args:
    relation: :hasRelation
    source: :Claude_of_Orleans
    target: :Enrico_Gandolfi
  Finish (28d0c923-b76a-4672-8244-75b39040887b)
 Call ID: 28d0c923-b76a-4672-8244-75b39040887b
  Args: