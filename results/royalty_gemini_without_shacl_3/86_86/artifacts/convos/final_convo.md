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
Prince Aimone, 4th Duke of Aosta (Aimone Roberto Margherita Maria Giuseppe Torino; 9 March 1900 – 29 January 1948), was a prince of Italy's reigning House of Savoy and an officer of the Royal Italian Navy.
The second son of Prince Emanuele Filiberto, Duke of Aosta, he was granted the title Duke of Spoleto on 22 September 1904.
He inherited the title Duke of Aosta on 3 March 1942 following the death of his brother Prince Amedeo in a British prisoner of war camp in Nairobi.
From 18 May 1941 to 31 July 1943, Aimone was designated king of the Independent State of Croatia (Croatian: Nezavisna Država Hrvatska, NDH), even though he never ruled there.
After the dismissal of Mussolini on 25 July 1943, Aimone abdicated on 31 July as king on the orders of Victor Emmanuel III.
Early life

Prince Aimone Roberto Margherita Maria Giuseppe Torino of Savoy-Aosta was born in Turin the second son of Prince Emanuele Filiberto, Duke of Aosta (eldest son of Prince Amedeo, 1st Duke of Aosta (and sometime "King Amadeo I of Spain") by his wife, née Vittoria dal Pozzo, Principessa della Cisterna) and Princess Hélène of Orléans (daughter of Philippe, comte de Paris, and Princess Marie Isabelle of Orléans).
With his brother Amedeo, he was educated at St  David's College, Reigate, Surrey, England, and Aimone later went to study at the naval academy in Livorno.
On 1 April 1921, Prince Aimone became a member of the Italian Senate.
In 1929, twenty years after his uncle Prince Luigi Amedeo, Duke of the Abruzzi had attempted to climb K2 in Karakoram, Prince Aimone led an expedition to Karakorum.
Due to the failure to climb K2 twenty years earlier, Prince Aimone's expedition concentrated solely on scientific work.
Marriage and issue

After being romantically linked with Infanta Beatriz of Spain, the daughter of King Alfonso XIII, he married, on 1 July 1939 at the church of Santa Maria del Fiore, Florence, Princess Irene of Greece and Denmark, daughter of King Constantine I and Princess Sophie of Prussia.
They had one son, Prince Amedeo, Duke of Aosta, born in 1943.
Aimone was then officially named king by his cousin Victor Emmanuel III.
The Italian Foreign Minister and Benito Mussolini's son in law Count Ciano's informants said of Aimone "The Duke doesn't give a damn about Croatia and wants only money, money and more money."
Ciano's diary noted a conversation between Aimone and himself, where Aimone was "proud of having been chosen King of Croatia, but has no exact idea of what he is supposed to do and is vaguely uneasy about it".
Aimone felt that Dalmatia "was a land that could never be Italianized" and was an obstacle to Italo-Croatian reconciliation.
Prince Aimone also established a Croatian office in Rome where he received confidential reports, official documents, and military, political and economic information from Croatia.
After the fall of the Fascist regime in Italy, Aimone abdicated as king of Croatia on 31 July 1943 on the orders of Victor Emmanuel III.
Prince Aimone succeeded to the title duke of Aosta on 3 March 1942, following the death of his elder brother Prince Amedeo, 3rd Duke of Aosta, in a British prisoner of war camp in Kenya.
In the autumn of 1942, Aimone contacted Allied forces via his courier, the consul general Alessandro Marieni, about the possibility of a peace settlement between Italy and Allied forces.
Death

In 1947, following the birth of the Italian Republic the previous year, Prince Aimone left Italy for South America.
The claim to the Aosta ducal title passed to his son Prince Amedeo.
}} Media related to Prince Aimone, Duke of Aosta at Wikimedia Commons



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
  AssignClass (83488666-15fb-4c5e-a4ea-17d0e1412def)
 Call ID: 83488666-15fb-4c5e-a4ea-17d0e1412def
  Args:
    source: :Aimone_4th_Duke_of_Aosta
    type: :Man
  AssignClass (fe8fb3b7-a464-4e2a-a292-c881eb3ec01f)
 Call ID: fe8fb3b7-a464-4e2a-a292-c881eb3ec01f
  Args:
    type: :Person
    source: :Aimone_4th_Duke_of_Aosta
  AddLiteral (e2d5bffe-cbe8-4250-a874-53b1c7d89313)
 Call ID: e2d5bffe-cbe8-4250-a874-53b1c7d89313
  Args:
    source: :Aimone_4th_Duke_of_Aosta
    literal_type: xsd:integer
    literal_value: 1900
    relation: :hasBirthYear
  AddLiteral (cf2b522c-afdc-4dec-8690-a9051070d1d7)
 Call ID: cf2b522c-afdc-4dec-8690-a9051070d1d7
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1948
    source: :Aimone_4th_Duke_of_Aosta
  AssignClass (2f7c09ea-702c-4635-89b4-0743986dc1df)
 Call ID: 2f7c09ea-702c-4635-89b4-0743986dc1df
  Args:
    source: :Emanuele_Filiberto_Duke_of_Aosta
    type: :Man
  AssignClass (8d5dcedf-4869-4930-8db2-57bb1e22c22f)
 Call ID: 8d5dcedf-4869-4930-8db2-57bb1e22c22f
  Args:
    type: :Person
    source: :Emanuele_Filiberto_Duke_of_Aosta
  AddTriple (699c2d3a-d243-4b29-9d98-7e9e1bf317b3)
 Call ID: 699c2d3a-d243-4b29-9d98-7e9e1bf317b3
  Args:
    relation: :hasFather
    target: :Emanuele_Filiberto_Duke_of_Aosta
    source: :Aimone_4th_Duke_of_Aosta
  AssignClass (52df990a-0cb1-4228-986d-27d920c2ceaf)
 Call ID: 52df990a-0cb1-4228-986d-27d920c2ceaf
  Args:
    type: :Man
    source: :Amedeo_3rd_Duke_of_Aosta
  AssignClass (6a0d56f4-f011-46e1-bce7-94a166f963d1)
 Call ID: 6a0d56f4-f011-46e1-bce7-94a166f963d1
  Args:
    source: :Amedeo_3rd_Duke_of_Aosta
    type: :Person
  AddTriple (ce90469c-4338-43b4-af07-8ac4c3267001)
 Call ID: ce90469c-4338-43b4-af07-8ac4c3267001
  Args:
    target: :Amedeo_3rd_Duke_of_Aosta
    source: :Aimone_4th_Duke_of_Aosta
    relation: :hasBrother
  AssignClass (b94b9fcd-68d6-4128-bb87-c3b74f6c5e72)
 Call ID: b94b9fcd-68d6-4128-bb87-c3b74f6c5e72
  Args:
    source: :Princess_Helene_of_Orleans
    type: :Woman
  AssignClass (d8b512f0-0408-4a6e-a3ef-71f8420c8d74)
 Call ID: d8b512f0-0408-4a6e-a3ef-71f8420c8d74
  Args:
    source: :Princess_Helene_of_Orleans
    type: :Person
  AddTriple (470baff4-7a15-4124-b456-9e562ffc0d81)
 Call ID: 470baff4-7a15-4124-b456-9e562ffc0d81
  Args:
    source: :Aimone_4th_Duke_of_Aosta
    target: :Princess_Helene_of_Orleans
    relation: :hasMother
  AssignClass (ce78e5f8-4eee-4d8a-944e-8322ba4612f3)
 Call ID: ce78e5f8-4eee-4d8a-944e-8322ba4612f3
  Args:
    source: :Amedeo_1st_Duke_of_Aosta
    type: :Man
  AssignClass (4563b5a2-d0b3-4ded-860b-97942e12987a)
 Call ID: 4563b5a2-d0b3-4ded-860b-97942e12987a
  Args:
    source: :Amedeo_1st_Duke_of_Aosta
    type: :Person
  AddTriple (ee594c81-4282-4b5b-8abe-dcd36dfbf3f3)
 Call ID: ee594c81-4282-4b5b-8abe-dcd36dfbf3f3
  Args:
    target: :Amedeo_1st_Duke_of_Aosta
    source: :Emanuele_Filiberto_Duke_of_Aosta
    relation: :hasFather
  AssignClass (0b0b44b4-dd9f-4e04-a36f-7b14145c1345)
 Call ID: 0b0b44b4-dd9f-4e04-a36f-7b14145c1345
  Args:
    type: :Woman
    source: :Vittoria_dal_Pozzo
  AssignClass (ae3840f4-dd90-4d6c-ac75-aeab2362f6de)
 Call ID: ae3840f4-dd90-4d6c-ac75-aeab2362f6de
  Args:
    type: :Person
    source: :Vittoria_dal_Pozzo
  AddTriple (112a3da9-8044-4cf6-83e7-764001a26e55)
 Call ID: 112a3da9-8044-4cf6-83e7-764001a26e55
  Args:
    relation: :hasMother
    target: :Vittoria_dal_Pozzo
    source: :Emanuele_Filiberto_Duke_of_Aosta
  AssignClass (4fe6bf7e-da2d-4795-bc26-613f3a18fe95)
 Call ID: 4fe6bf7e-da2d-4795-bc26-613f3a18fe95
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    type: :Woman
  AssignClass (d7a64058-8ac6-4ae2-b8e2-7403273135a0)
 Call ID: d7a64058-8ac6-4ae2-b8e2-7403273135a0
  Args:
    type: :Person
    source: :Princess_Irene_of_Greece_and_Denmark
  AddTriple (1ad879b6-9a2a-4409-9211-c3a4c06f8a01)
 Call ID: 1ad879b6-9a2a-4409-9211-c3a4c06f8a01
  Args:
    source: :Aimone_4th_Duke_of_Aosta
    target: :Princess_Irene_of_Greece_and_Denmark
    relation: :hasRelation
  AddLiteral (4ab6eb69-611d-419d-8a0c-1788c376a07e)
 Call ID: 4ab6eb69-611d-419d-8a0c-1788c376a07e
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1939
    source: :Aimone_4th_Duke_of_Aosta
  AssignClass (5f3f6d41-74c4-4c86-8461-f89d387ef366)
 Call ID: 5f3f6d41-74c4-4c86-8461-f89d387ef366
  Args:
    source: :Amedeo_Prince_Duke_of_Aosta_son
    type: :Man
  AssignClass (d4e03e7a-8fa2-4e9c-aeac-e6a57c391db9)
 Call ID: d4e03e7a-8fa2-4e9c-aeac-e6a57c391db9
  Args:
    type: :Person
    source: :Amedeo_Prince_Duke_of_Aosta_son
  AddTriple (e41188e2-bfd2-4acc-95a5-4ef08a6ec24e)
 Call ID: e41188e2-bfd2-4acc-95a5-4ef08a6ec24e
  Args:
    relation: :hasFather
    target: :Aimone_4th_Duke_of_Aosta
    source: :Amedeo_Prince_Duke_of_Aosta_son
  AddTriple (2ea206be-48b4-4641-b61e-2f2c5bd9dc10)
 Call ID: 2ea206be-48b4-4641-b61e-2f2c5bd9dc10
  Args:
    source: :Amedeo_Prince_Duke_of_Aosta_son
    target: :Princess_Irene_of_Greece_and_Denmark
    relation: :hasMother
  Finish (96fd0284-9fc0-4d94-9102-f4397bd6aabe)
 Call ID: 96fd0284-9fc0-4d94-9102-f4397bd6aabe
  Args: