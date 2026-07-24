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
  AssignClass (1be2923e-f98a-44c2-a5be-d1eb33787b4c)
 Call ID: 1be2923e-f98a-44c2-a5be-d1eb33787b4c
  Args:
    type: :Woman
    source: Princess_Claude_of_Orléans
  AssignClass (d8b156a2-22a3-48bb-a4e7-68ffd48a079e)
 Call ID: d8b156a2-22a3-48bb-a4e7-68ffd48a079e
  Args:
    source: Princess_Claude_of_Orléans
    type: :Person
  AddLiteral (e50136bb-6025-4d09-9b52-264f1d5a540d)
 Call ID: e50136bb-6025-4d09-9b52-264f1d5a540d
  Args:
    literal_value: 1943
    literal_type: xsd:integer
    source: Princess_Claude_of_Orléans
    relation: :hasBirthYear
  AssignClass (22d2c101-d90a-4cbd-b4aa-909d21b132eb)
 Call ID: 22d2c101-d90a-4cbd-b4aa-909d21b132eb
  Args:
    source: Henri_Count_of_Paris
    type: :Man
  AssignClass (8ad16721-850c-46d9-8899-590545cf59e7)
 Call ID: 8ad16721-850c-46d9-8899-590545cf59e7
  Args:
    type: :Ancestor
    source: Henri_Count_of_Paris
  AssignClass (909dca87-04d9-4ec1-8fc9-ec7c88c2b9ea)
 Call ID: 909dca87-04d9-4ec1-8fc9-ec7c88c2b9ea
  Args:
    type: :Person
    source: Henri_Count_of_Paris
  AssignClass (1c0d190f-77db-4291-ba59-4afdb37d5846)
 Call ID: 1c0d190f-77db-4291-ba59-4afdb37d5846
  Args:
    source: Princess_Isabelle_of_Orléans-Braganza
    type: :Woman
  AssignClass (8552abe3-b3bc-47a7-8805-2260db1ead32)
 Call ID: 8552abe3-b3bc-47a7-8805-2260db1ead32
  Args:
    source: Princess_Isabelle_of_Orléans-Braganza
    type: :Ancestor
  AssignClass (99c3a53f-d411-48ad-972d-972d3b21d6d7)
 Call ID: 99c3a53f-d411-48ad-972d-972d3b21d6d7
  Args:
    type: :Person
    source: Princess_Isabelle_of_Orléans-Braganza
  AddTriple (a46592a9-11f8-44d1-a8b0-91f80057058c)
 Call ID: a46592a9-11f8-44d1-a8b0-91f80057058c
  Args:
    target: Henri_Count_of_Paris
    relation: :hasFather
    source: Princess_Claude_of_Orléans
  AddTriple (d0951bb6-79fc-4392-ae3d-63c3e18ddcf0)
 Call ID: d0951bb6-79fc-4392-ae3d-63c3e18ddcf0
  Args:
    relation: :hasMother
    source: Princess_Claude_of_Orléans
    target: Princess_Isabelle_of_Orléans-Braganza
  AssignClass (ef9dce9e-b66d-4982-9ed2-f19ab002b37e)
 Call ID: ef9dce9e-b66d-4982-9ed2-f19ab002b37e
  Args:
    source: Henri_Count_of_Paris_jr
    type: :Man
  AssignClass (e2ad1fc8-70cb-4a03-8d3f-0f56954ad796)
 Call ID: e2ad1fc8-70cb-4a03-8d3f-0f56954ad796
  Args:
    source: Henri_Count_of_Paris_jr
    type: :Person
  AddTriple (84ddc596-7426-44fc-9e91-916a4ca1e4d6)
 Call ID: 84ddc596-7426-44fc-9e91-916a4ca1e4d6
  Args:
    target: Henri_Count_of_Paris_jr
    relation: :hasBrother
    source: Princess_Claude_of_Orléans
  AssignClass (81cf3e76-2396-44ff-8bbb-80a35f755f07)
 Call ID: 81cf3e76-2396-44ff-8bbb-80a35f755f07
  Args:
    type: :Woman
    source: Anne_Duchess_of_Calabria
  AssignClass (c3f13678-3a5f-43cc-9ec1-1ae4aa254b29)
 Call ID: c3f13678-3a5f-43cc-9ec1-1ae4aa254b29
  Args:
    source: Anne_Duchess_of_Calabria
    type: :Person
  AddTriple (97b6ee15-299b-45ac-a338-8dcbcd18a465)
 Call ID: 97b6ee15-299b-45ac-a338-8dcbcd18a465
  Args:
    target: Anne_Duchess_of_Calabria
    relation: :hasSister
    source: Princess_Claude_of_Orléans
  AssignClass (cbc65de3-a64e-4a3b-9d65-e6976a72e724)
 Call ID: cbc65de3-a64e-4a3b-9d65-e6976a72e724
  Args:
    type: :Woman
    source: Diane_Duchess_of_Württemberg
  AssignClass (60c45e29-11f1-4f5c-9042-5c36f7360ffc)
 Call ID: 60c45e29-11f1-4f5c-9042-5c36f7360ffc
  Args:
    source: Diane_Duchess_of_Württemberg
    type: :Person
  AddTriple (df6acd29-2b8c-49cf-a47d-fed1743d49e3)
 Call ID: df6acd29-2b8c-49cf-a47d-fed1743d49e3
  Args:
    relation: :hasSister
    source: Princess_Claude_of_Orléans
    target: Diane_Duchess_of_Württemberg
  AssignClass (17f52b8f-a583-4b68-ae64-7b712be8e301)
 Call ID: 17f52b8f-a583-4b68-ae64-7b712be8e301
  Args:
    source: Prince_Amedeo_of_Savoy_Duke_of_Aosta
    type: :Man
  AssignClass (4ff1e486-5f93-4001-b930-80df17f3c6f2)
 Call ID: 4ff1e486-5f93-4001-b930-80df17f3c6f2
  Args:
    source: Prince_Amedeo_of_Savoy_Duke_of_Aosta
    type: :Person
  AddTriple (167e9efc-9762-4984-be34-a8bca0e70070)
 Call ID: 167e9efc-9762-4984-be34-a8bca0e70070
  Args:
    target: Prince_Amedeo_of_Savoy_Duke_of_Aosta
    source: Princess_Claude_of_Orléans
    relation: :hasRelation
  AssignClass (e2b31d0a-a9cc-4d3d-9373-c1a45153910e)
 Call ID: e2b31d0a-a9cc-4d3d-9373-c1a45153910e
  Args:
    type: :Man
    source: Prince_Aimone_Duke_of_Aosta
  AssignClass (9a029786-a516-4bdf-a8b2-8b28409f8c43)
 Call ID: 9a029786-a516-4bdf-a8b2-8b28409f8c43
  Args:
    source: Prince_Aimone_Duke_of_Aosta
    type: :Ancestor
  AssignClass (daa51e14-477b-4c2f-9025-cb3090fb12fa)
 Call ID: daa51e14-477b-4c2f-9025-cb3090fb12fa
  Args:
    source: Prince_Aimone_Duke_of_Aosta
    type: :Person
  AddTriple (c078e781-b95a-490d-9182-c1d5bd15d4bf)
 Call ID: c078e781-b95a-490d-9182-c1d5bd15d4bf
  Args:
    target: Prince_Aimone_Duke_of_Aosta
    source: Prince_Amedeo_of_Savoy_Duke_of_Aosta
    relation: :hasFather
  AssignClass (3a00d8df-3c1a-405a-bdcc-0803309a174f)
 Call ID: 3a00d8df-3c1a-405a-bdcc-0803309a174f
  Args:
    source: Luigi_Arnaldo_La_Cagnina
    type: :Man
  AssignClass (67fca71f-2dea-4c5e-8ee9-c954ac4b0647)
 Call ID: 67fca71f-2dea-4c5e-8ee9-c954ac4b0647
  Args:
    source: Luigi_Arnaldo_La_Cagnina
    type: :Person
  AddTriple (55c46072-116e-4c23-aaba-7223d5ce6c69)
 Call ID: 55c46072-116e-4c23-aaba-7223d5ce6c69
  Args:
    target: Luigi_Arnaldo_La_Cagnina
    source: Princess_Claude_of_Orléans
    relation: :hasRelation
  AssignClass (1b4b9fc8-74cd-4cb1-b919-77dbaddf18c3)
 Call ID: 1b4b9fc8-74cd-4cb1-b919-77dbaddf18c3
  Args:
    type: :Man
    source: Enrico_Gandolfi
  AssignClass (23e8833d-1701-429e-a42a-7be7bc823a4c)
 Call ID: 23e8833d-1701-429e-a42a-7be7bc823a4c
  Args:
    type: :Person
    source: Enrico_Gandolfi
  AddTriple (634c4f59-67cc-4ff2-8b1f-eb003477b920)
 Call ID: 634c4f59-67cc-4ff2-8b1f-eb003477b920
  Args:
    target: Enrico_Gandolfi
    source: Princess_Claude_of_Orléans
    relation: :hasRelation
  AssignClass (29215992-07de-45ac-a625-b50432355fea)
 Call ID: 29215992-07de-45ac-a625-b50432355fea
  Args:
    source: Silvia_Paternò_di_Spedalotto
    type: :Woman
  AssignClass (170567c1-33dd-4778-87e1-f13b708970d9)
 Call ID: 170567c1-33dd-4778-87e1-f13b708970d9
  Args:
    type: :Person
    source: Silvia_Paternò_di_Spedalotto
  AddTriple (7e6f4f75-356b-4de1-918e-7b0c019b37ae)
 Call ID: 7e6f4f75-356b-4de1-918e-7b0c019b37ae
  Args:
    source: Prince_Amedeo_of_Savoy_Duke_of_Aosta
    relation: :hasRelation
    target: Silvia_Paternò_di_Spedalotto
  Finish (f9d12ab5-550b-4131-8581-85a43a8905ab)
 Call ID: f9d12ab5-550b-4131-8581-85a43a8905ab
  Args: