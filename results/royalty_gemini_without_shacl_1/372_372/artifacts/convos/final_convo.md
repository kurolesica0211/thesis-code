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
Prince George William of Hanover and Cumberland (Georg Wilhelm Ernst August Friedrich Axel Prinz von Hannover; 25 March 1915 – 8 January 2006) was the second-eldest son of Ernest Augustus, Duke of Brunswick, and his wife Princess Victoria Louise of Prussia, the only daughter of Wilhelm II, German Emperor, and Augusta Victoria of Schleswig-Holstein.
George William's wife was a sister of Prince Philip, Duke of Edinburgh, and his children are thus first cousins of King Charles III.
His sister, Frederica, became Queen of the Hellenes as the consort of King Paul of Greece.
He held the title of Prince of the United Kingdom of Great Britain and Ireland, granted ad personam to the children of the then-Duke of Brunswick by George V's letters patent of 1914, which remained unrevoked.
Life

George William was christened on 10 May 1915 in Brunswick.
The prince's godparents included Maria Christina of Austria, Prince Axel of Denmark, and Princess Olga of Hanover and Cumberland who held the infant prince over the baptismal font.
From 1930 through 1934, Prince George William attended the elite boarding school Schule Schloss Salem in Überlingen on Lake Constance.
Schule Schloss Salem was co-founded by the prince's uncle, the last Chancellor of the German Empire, Prince Maximilian of Baden, and educator Kurt Hahn in 1920.
A former student of the institution, the prince then went to Scotland with his wife to meet with Kurt Hahn, the founder of the school, and to visit Gordonstoun, the establishment that the latter founded when he had to flee Nazi Germany because of his Jewish origins.
Together with his wife, as well as his three brothers, he took part in the ship tours organized by his sister Queen Frederica and her husband King Paul of Greece in 1954 and 1956, which became known as the “Cruises of the Kings” and were attended by over 100 royals from all over Europe.
For many years Prince George William was a member of the International Olympic Committee (IOC) and of the Deutscher Olympischer Sportbund (DOSB), the German NOC.
Prince George William of Hanover lived in Schliersee, near Munich, and died in Munich in 2006 aged 90.
His wife, Sophie, sister of Prince Philip of Greece and Denmark, later Duke of Edinburgh, consort of Queen Elizabeth II of the United Kingdom, died in 2001.
Marriage

On 23 April 1946 in Salem, Baden-Württemberg, Germany, Prince George William married his third cousin Princess Sophie of Greece and Denmark, daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, and the widow of Prince Christoph of Hesse.
After consultations with the Foreign Office, Home Office and King George VI's private secretary, Sir Alan Lascelles, a ciphered telegram dated 18 April 1946 and crafted by Sir Albert Napier, permanent secretary to the Lord Chancellor, was transmitted from the British Foreign Office to the Foreign Adviser to the British Commander in Chief at Berlin:


"The Duke of Brunswick has formally applied to The King by letter of March 22nd for the consent of His Majesty under the Act 12 Geo.
11 to the marriage of his son Prince George William with Princess Sophia Dowager Princess of Hesse.
Please convey to the Duke an informal intimation that in view of the fact that a state of war still exists between Great Britain and Germany, His Majesty is advised that the case is not one in which it is practicable for His consent to be given in the manner contemplated by the Act.
"

They had three children: Welf (1947–1981), Georg (born 1949) and Friederike (born 1954).
Ancestry

George William was a descendant of Victoria of the United Kingdom and Albert, Prince Consort through their eldest daughter Victoria, Princess Royal, the wife of Frederick III, German Emperor.
He was born a Prince of the United Kingdom of Great Britain and Ireland.



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
  AssignClass (f86518ea-d5ba-47c2-ae85-48e596aa7780)
 Call ID: f86518ea-d5ba-47c2-ae85-48e596aa7780
  Args:
    type: :Man
    source: :GeorgeWilliamOfHanover
  AssignClass (5f762008-ffc7-4d8e-b6ef-73b975adecb3)
 Call ID: 5f762008-ffc7-4d8e-b6ef-73b975adecb3
  Args:
    type: :Man
    source: :ErnestAugustusDukeOfBrunswick
  AssignClass (e76aa231-1328-4c5c-af9f-19163bab088a)
 Call ID: e76aa231-1328-4c5c-af9f-19163bab088a
  Args:
    type: :Woman
    source: :VictoriaLouiseOfPrussia
  AssignClass (aed9c4d9-f121-4189-ac23-1686bc103100)
 Call ID: aed9c4d9-f121-4189-ac23-1686bc103100
  Args:
    type: :Man
    source: :WilhelmII
  AssignClass (73855d0c-c038-4f83-9d95-b95df87f7e5f)
 Call ID: 73855d0c-c038-4f83-9d95-b95df87f7e5f
  Args:
    type: :Woman
    source: :AugustaVictoriaOfSchleswigHolstein
  AssignClass (ad55f5af-415d-4640-9e2f-edca0097138c)
 Call ID: ad55f5af-415d-4640-9e2f-edca0097138c
  Args:
    type: :Woman
    source: :FredericaOfHanover
  AssignClass (58aaec37-fe5b-4afb-ad3f-5cba56889ec6)
 Call ID: 58aaec37-fe5b-4afb-ad3f-5cba56889ec6
  Args:
    type: :Man
    source: :PaulOfGreece
  AssignClass (1baf2c9d-4bc4-4e8c-96af-73546ad38fb7)
 Call ID: 1baf2c9d-4bc4-4e8c-96af-73546ad38fb7
  Args:
    type: :Woman
    source: :SophieOfGreeceAndDenmark
  AssignClass (1a0ee0cf-fa34-4704-9112-0081e92886d8)
 Call ID: 1a0ee0cf-fa34-4704-9112-0081e92886d8
  Args:
    type: :Man
    source: :AndrewOfGreeceAndDenmark
  AssignClass (495a55bc-9a49-4a7b-bd01-d86b43931853)
 Call ID: 495a55bc-9a49-4a7b-bd01-d86b43931853
  Args:
    type: :Woman
    source: :AliceOfBattenberg
  AssignClass (1ef207ef-5ae4-4fb5-b3c8-ca24f13c6854)
 Call ID: 1ef207ef-5ae4-4fb5-b3c8-ca24f13c6854
  Args:
    type: :Man
    source: :WelfOfHanover
  AssignClass (d5d1cd11-6b9a-4813-bac7-f6b2c72c259c)
 Call ID: d5d1cd11-6b9a-4813-bac7-f6b2c72c259c
  Args:
    type: :Man
    source: :GeorgOfHanover
  AssignClass (2c198766-4907-4fa5-9aea-34b4d422e00f)
 Call ID: 2c198766-4907-4fa5-9aea-34b4d422e00f
  Args:
    type: :Woman
    source: :FriederikeOfHanover
  AddLiteral (47565e60-be3e-4ac2-ab59-73413b3398bb)
 Call ID: 47565e60-be3e-4ac2-ab59-73413b3398bb
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :GeorgeWilliamOfHanover
    literal_value: 1915
  AddLiteral (35d540a9-dcc5-4ed1-8d2f-7199e56d2617)
 Call ID: 35d540a9-dcc5-4ed1-8d2f-7199e56d2617
  Args:
    source: :GeorgeWilliamOfHanover
    literal_value: 2006
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (1040eb56-5b21-40f1-90e5-eb5b8f5950de)
 Call ID: 1040eb56-5b21-40f1-90e5-eb5b8f5950de
  Args:
    source: :GeorgeWilliamOfHanover
    relation: :hasFather
    target: :ErnestAugustusDukeOfBrunswick
  AddTriple (331bea7c-6461-4253-883e-5ee3a8e14cef)
 Call ID: 331bea7c-6461-4253-883e-5ee3a8e14cef
  Args:
    source: :GeorgeWilliamOfHanover
    relation: :hasMother
    target: :VictoriaLouiseOfPrussia
  AddTriple (a5c2b7fd-3e93-40bf-b813-bbb54986df7a)
 Call ID: a5c2b7fd-3e93-40bf-b813-bbb54986df7a
  Args:
    relation: :hasFather
    target: :WilhelmII
    source: :VictoriaLouiseOfPrussia
  AddTriple (b9f5ed66-374b-4ed8-862a-6eb798720715)
 Call ID: b9f5ed66-374b-4ed8-862a-6eb798720715
  Args:
    target: :AugustaVictoriaOfSchleswigHolstein
    relation: :hasMother
    source: :VictoriaLouiseOfPrussia
  AddTriple (3b6f3ba9-c5be-4835-bcf2-b576b8e545f0)
 Call ID: 3b6f3ba9-c5be-4835-bcf2-b576b8e545f0
  Args:
    source: :GeorgeWilliamOfHanover
    relation: :hasSister
    target: :FredericaOfHanover
  AddTriple (7d58b4ec-2efe-4ac2-beb5-a5068159b709)
 Call ID: 7d58b4ec-2efe-4ac2-beb5-a5068159b709
  Args:
    source: :SophieOfGreeceAndDenmark
    relation: :hasFather
    target: :AndrewOfGreeceAndDenmark
  AddTriple (1800d50b-f09b-421b-abbb-a80b66f4ee67)
 Call ID: 1800d50b-f09b-421b-abbb-a80b66f4ee67
  Args:
    source: :SophieOfGreeceAndDenmark
    target: :AliceOfBattenberg
    relation: :hasMother
  AddTriple (aa1bce8a-bbe1-4814-86e9-3a2ffcd27eb1)
 Call ID: aa1bce8a-bbe1-4814-86e9-3a2ffcd27eb1
  Args:
    source: :GeorgeWilliamOfHanover
    target: :WelfOfHanover
    relation: :hasChild
  AddTriple (bf81fd7c-d19e-4eff-9e8d-c086bd98c317)
 Call ID: bf81fd7c-d19e-4eff-9e8d-c086bd98c317
  Args:
    source: :GeorgeWilliamOfHanover
    target: :GeorgOfHanover
    relation: :hasChild
  AddTriple (ac1ea7ba-c157-446d-90d3-3c8517412231)
 Call ID: ac1ea7ba-c157-446d-90d3-3c8517412231
  Args:
    target: :FriederikeOfHanover
    relation: :hasChild
    source: :GeorgeWilliamOfHanover
  AddTriple (6ca1d89e-29be-43a4-985c-386ecb070e7e)
 Call ID: 6ca1d89e-29be-43a4-985c-386ecb070e7e
  Args:
    relation: :hasChild
    target: :WelfOfHanover
    source: :SophieOfGreeceAndDenmark
  AddTriple (e18cec3a-af48-4310-b7ac-9cd4352aadc2)
 Call ID: e18cec3a-af48-4310-b7ac-9cd4352aadc2
  Args:
    relation: :hasChild
    target: :GeorgOfHanover
    source: :SophieOfGreeceAndDenmark
  AddTriple (35fcd27a-053e-45a2-9aa0-c8d4fb694b44)
 Call ID: 35fcd27a-053e-45a2-9aa0-c8d4fb694b44
  Args:
    relation: :hasChild
    target: :FriederikeOfHanover
    source: :SophieOfGreeceAndDenmark
  AddLiteral (583c1a7d-06e7-4888-bb08-3131e161e890)
 Call ID: 583c1a7d-06e7-4888-bb08-3131e161e890
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :GeorgeWilliamOfHanover
    literal_value: 1946
  AddLiteral (6554be7e-4d1e-4791-b3cd-1f1cd2c6d3be)
 Call ID: 6554be7e-4d1e-4791-b3cd-1f1cd2c6d3be
  Args:
    literal_value: 1947
    source: :WelfOfHanover
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (de6fc1cc-339d-4c1e-ad1d-ef53cef1c8a1)
 Call ID: de6fc1cc-339d-4c1e-ad1d-ef53cef1c8a1
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :WelfOfHanover
    literal_value: 1981
  AddLiteral (b3a1c810-13a8-4948-b693-35f3d0a7e7db)
 Call ID: b3a1c810-13a8-4948-b693-35f3d0a7e7db
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1949
    source: :GeorgOfHanover
  AddLiteral (35558e79-1bcf-48cb-9355-f3bd7edf02cc)
 Call ID: 35558e79-1bcf-48cb-9355-f3bd7edf02cc
  Args:
    literal_value: 1954
    source: :FriederikeOfHanover
    relation: :hasBirthYear
    literal_type: xsd:integer
  Finish (93297130-8c0a-4c32-b9d1-de66ed8c7efc)
 Call ID: 93297130-8c0a-4c32-b9d1-de66ed8c7efc
  Args: