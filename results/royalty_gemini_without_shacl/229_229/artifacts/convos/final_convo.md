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
Henri Philippe Pierre Marie d'Orléans (14 June 1933 – 21 January 2019) was the Orléanist pretender to the defunct French throne as Henry VII.
Henri was a retired military officer as well as an author and painter.
Early life

He was the first son of Henri, Count of Paris (1908–1999), and his wife Princess Isabelle of Orléans-Braganza, and was born in Woluwe-Saint-Pierre, Belgium, a law in 1886 having permanently exiled from France the heads of its formerly reigning dynasties and their eldest sons.
Despite the ban, while living in Belgium Henri occasionally accompanied his mother on brief visits to France and, later, to his mother's relatives in Brazil.
While his father sought to play a role in the French resistance, Henri, in 1940 a child of 7, remained at Larache with his mother, siblings, grandmother and father's sisters' families during the Nazi occupation of France, sharing a small desert home that lacked electricity.
Advised by Henri Giraud's Moroccan command that the Orléans had become unwelcome in the protectorate following the assassination of Vichy regime collaborater François Darlan by the monarchist Fernand Bonnier de La Chapelle, the family relocated to Pamplona in Spain until 1947, when they took up residence at the Quinta do Anjinho, an estate near Sintra, on the Portuguese Riviera.
During that year, President Vincent Auriol allowed Henri and his brother François to visit France, and in 1948 he was allowed to enroll in a lycée in Bordeaux.
The law of exile was abrogated in 1950, allowing Henri to repatriate with his parents.
Later that year, his parents purchased an estate near Paris, the Manoir du Cœur-Volant in Louveciennes, which became Henri's first home in France.
Henri studied at the Institut d'Études Politiques de Paris (Sciences Po), obtaining his bac in 1957, and on 30 June of that year, his father conferred upon him, as the heir apparent of his house, the title of "Count of Clermont", by which he was generally known during his father's lifetime.
Career

From October 1959 to April 1962, Henri worked at the Secretariat-General for National Defence and Security as a member of the French Foreign Legion.
Returning to civilian life in 1967, Henri and his family briefly occupied the Blanche Neige pavilion on the grounds of his father's Cœur-Volant estate before renting an apartment of their own in the 15th arrondissement of Paris.
Henri wrote several books, including:


Henri was also a painter and launched his own brand of perfume.
Marriages and children

Henri met Duchess Marie Therese of Württemberg (born 1934), like himself a descendant of King Louis-Philippe, at a ball given by the Thurn and Taxis family in Munich.
Five children were born from this union:


In 1984, Henri and Marie-Thérèse were divorced.
On 31 October 1984 Henri entered a civil marriage with Micaëla Anna María Cousiño y Quiñones de León (1938–2022), daughter of Luis Cousiño y Sebire and his wife, Antonia Maria Quiñones de Léon y Bañuelos, 4th Marquesa de San Carlos, and who had previously been divorced from Jean-Robert Bœuf.
For remarrying without consent, Henri's father initially declared him disinherited, substituting the non-dynastic title Comte de Mortain for his son's Clermont countship (the latter once held in appanage by a son of Louis IX of France, who became ancestor of the Bourbon-Orléans line).
Henri, though, refused all mail addressed to him as "Mortain".
On 27 February 1984 Marie-Thérèse, the former Countess of Clermont, was granted the title Duchess of Montpensier by her father-in-law.
On 11 February 1989 Henri was informed, by a hand-delivered letter written by his former wife, of the engagement of their eldest child Marie, to Prince Gundakar of Liechtenstein, a cousin of the ruler of that principality, the wedding date being set for 29 July 1989.
Although Henri acknowledged, in a 12 May 1989 Point de Vue interview, that it had been three years since he had seen Marie, he and his second wife, Micaëla Cousiño, had been welcomed for the first time to the home of his mother, the Countess of Paris, that day: Henri further acknowledged to the press that, Marie having written to invite him to her wedding, he looked forward to conducting her to the altar, rumours to the contrary notwithstanding.
At the engagement party held the next day at the Palais Pallavicini, the Vienna home of the fiancé's parents, photographs were taken, and would later be published, showing Henri speaking cordially with his daughter, sons, former wife and future son-in-law.
However, it was on this occasion that Henri learned that he would not be escorting Marie to her bridegroom during the wedding.
Meanwhile, Marie-Thérèse had sent out invitations to the wedding in her name alone, omitting not only mention of Marie's father, but also of her grandfather, Monseigneur the Count of Paris who, until then, had largely sided with the Duchess of Montpensier in family matters and had consented to his granddaughter's choice of a spouse.
Henri and his father refused to attend the wedding but Marie proceeded to marry civilly at Dreux's city hall on 22 July 1989, and religiously at the castle of her mother's brother in Germany, on 29 July 1989.
All but two of Henri's eight siblings also boycotted the ceremonies, but his sister Diane (wife of Montpensier's brother) hosted, and Henri's mother, Madame the Countess of Paris, was a guest at the religious wedding.
Tensions lessened after several years, and on 7 March 1991 Henri's father reinstated him as heir apparent and Count of Clermont, simultaneously giving Micaëla the title "Princesse de Joinville".
In 1980, Henri joined the Grand Orient de France where he became Grand Master of the regular Masonic Lodge "Lys de France" No 1297.
Head of house

Until he succeeded his father as royal claimant, Henri and his second wife occupied an apartment in Paris.
On 19 June 1999, Henri's father died and he became the new head of the House of Orléans.
He took the traditional title, Count of Paris, adding an ancient one, Duke of France, not borne by his Orléans or Bourbon forebears, but used a thousand years ago by his ancestors, before Hugh Capet took the title of king.
His wife assumed the title "Duchess of France", deferring to the continued use of "Countess of Paris" by Henri's widowed mother until her death on 5 July 2003, whereupon Micaela assumed that title.
After his father's death, Henri annulled his father's decision to deprive his brothers Michel (Count of Évreux) and Thibaut (the late Count of La Marche) of their succession rights because Michel married a French noblewoman without permission and because Thibaut married a commoner.
He also bestowed titles upon the sons of his brother Prince Jacques, Duke of Orléans: Prince Charles-Louis d'Orléans, Duke of Chartres (born 1972), and Prince Foulques d'Orléans, Duke of Aumale and Count of Eu (born 1974).
Henri recognised his disabled eldest son François as his dynastic heir-apparent, with the title Count of Clermont, declaring that François would exercise his prerogatives as head of the dynasty under the "regency" of his younger brother Prince Jean, Duke of Vendôme.
In 2009, Henri obtained an annulment of his marriage to Marie-Thérèse of Württemberg from the Holy See.
As Count of Paris, Henri took part in some European royal events attending, for instance, the 2011 marriage of Albert II of Monaco.
Legal cases

Prior to succeeding his father as royal claimant, Henri launched an unsuccessful court case (1987–1989) in which he challenged the right of his rival paternal 10th cousin Louis-Alphonse, Duke of Anjou, to use the undifferenced royal arms of France and the Anjou title.
The French courts dismissed the case on the grounds that Henri failed to prove that he had demonstrated a right to the hereditaments in questions, noting also that the court lacked jurisdiction in a dispute over dynastic claims of France's former royal family.
In 2000 bailiffs pursued Henri for US$143,000 back rent after he fled the Villa Boileau, a 17th-century Paris house he had occupied.



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
  AssignClass (e116f469-015b-4dfa-9d52-b703e9211cf4)
 Call ID: e116f469-015b-4dfa-9d52-b703e9211cf4
  Args:
    type: :Man
    source: :HenriPhilippePierreMariedOrleans
  AssignClass (2c16c0df-a765-4640-aec7-d33249f3c678)
 Call ID: 2c16c0df-a765-4640-aec7-d33249f3c678
  Args:
    source: :HenriPhilippePierreMariedOrleans
    type: :Person
  AddLiteral (6d9ec13b-df93-4919-8074-04ffd0e326e3)
 Call ID: 6d9ec13b-df93-4919-8074-04ffd0e326e3
  Args:
    literal_type: xsd:integer
    source: :HenriPhilippePierreMariedOrleans
    relation: :hasBirthYear
    literal_value: 1933
  AddLiteral (50af4eef-b817-4064-91d1-54f6a1dcd597)
 Call ID: 50af4eef-b817-4064-91d1-54f6a1dcd597
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :HenriPhilippePierreMariedOrleans
    literal_value: 2019
  AssignClass (2b8ee66a-d626-436d-9bcf-b03ec9f05d43)
 Call ID: 2b8ee66a-d626-436d-9bcf-b03ec9f05d43
  Args:
    source: :HenriCountOfParis
    type: :Man
  AssignClass (4a42fdc8-b81f-443b-a320-e3ef9772b617)
 Call ID: 4a42fdc8-b81f-443b-a320-e3ef9772b617
  Args:
    source: :HenriCountOfParis
    type: :Person
  AddLiteral (7c707477-27b0-46d3-b8c2-87dd47ac8876)
 Call ID: 7c707477-27b0-46d3-b8c2-87dd47ac8876
  Args:
    literal_value: 1908
    relation: :hasBirthYear
    source: :HenriCountOfParis
    literal_type: xsd:integer
  AddLiteral (485468c8-21b8-4d83-a62f-7eb69de9061e)
 Call ID: 485468c8-21b8-4d83-a62f-7eb69de9061e
  Args:
    relation: :hasDeathYear
    source: :HenriCountOfParis
    literal_value: 1999
    literal_type: xsd:integer
  AssignClass (5b03fcfc-411f-4e47-a9c9-17c55eecd025)
 Call ID: 5b03fcfc-411f-4e47-a9c9-17c55eecd025
  Args:
    type: :Woman
    source: :PrincessIsabelleOfOrleansBraganza
  AssignClass (b8c0f64f-5e8e-4fec-a273-45120a62460f)
 Call ID: b8c0f64f-5e8e-4fec-a273-45120a62460f
  Args:
    source: :PrincessIsabelleOfOrleansBraganza
    type: :Person
  AddTriple (110f95ae-9f14-47ad-bf2a-4b973c66ae3b)
 Call ID: 110f95ae-9f14-47ad-bf2a-4b973c66ae3b
  Args:
    relation: :hasFather
    source: :HenriPhilippePierreMariedOrleans
    target: :HenriCountOfParis
  AddTriple (a3a858ec-8a2e-428b-b001-1f51874a39a8)
 Call ID: a3a858ec-8a2e-428b-b001-1f51874a39a8
  Args:
    source: :HenriPhilippePierreMariedOrleans
    relation: :hasMother
    target: :PrincessIsabelleOfOrleansBraganza
  AssignClass (46b2fe2f-cd4f-4cc4-a124-1c2195017f7a)
 Call ID: 46b2fe2f-cd4f-4cc4-a124-1c2195017f7a
  Args:
    source: :FrancoisBrotherOfHenri
    type: :Man
  AssignClass (e40b9ae7-2572-48f6-979b-ea5287f5108c)
 Call ID: e40b9ae7-2572-48f6-979b-ea5287f5108c
  Args:
    type: :Person
    source: :FrancoisBrotherOfHenri
  AddTriple (e64ead5c-fcbb-4eed-b40a-de074e2d9bf9)
 Call ID: e64ead5c-fcbb-4eed-b40a-de074e2d9bf9
  Args:
    target: :FrancoisBrotherOfHenri
    source: :HenriPhilippePierreMariedOrleans
    relation: :isSiblingOf
  AssignClass (71f1edcc-24c9-42f3-87a6-46522bccc470)
 Call ID: 71f1edcc-24c9-42f3-87a6-46522bccc470
  Args:
    source: :MarieThereseOfWurttemberg
    type: :Woman
  AssignClass (81a0ccc9-14eb-463d-86cf-4d19b084f9b2)
 Call ID: 81a0ccc9-14eb-463d-86cf-4d19b084f9b2
  Args:
    source: :MarieThereseOfWurttemberg
    type: :Person
  AddLiteral (047cdf1d-5550-407a-bb1f-3e55701b335b)
 Call ID: 047cdf1d-5550-407a-bb1f-3e55701b335b
  Args:
    relation: :hasBirthYear
    source: :MarieThereseOfWurttemberg
    literal_value: 1934
    literal_type: xsd:integer
  AddTriple (2d11c95e-5611-4474-8bf6-c49b45553fb0)
 Call ID: 2d11c95e-5611-4474-8bf6-c49b45553fb0
  Args:
    relation: :hasRelation
    source: :HenriPhilippePierreMariedOrleans
    target: :MarieThereseOfWurttemberg
  AddLiteral (9e4903b0-56b8-41e9-a71a-d5526688636c)
 Call ID: 9e4903b0-56b8-41e9-a71a-d5526688636c
  Args:
    literal_type: xsd:integer
    literal_value: 1984
    relation: :hasMarriageYear
    source: :HenriPhilippePierreMariedOrleans
  AssignClass (bd4d29b1-a648-4b28-a41a-47fcf6e9a235)
 Call ID: bd4d29b1-a648-4b28-a41a-47fcf6e9a235
  Args:
    source: :MicaelaAnnaMariaCousinoYQuinonesDeLeon
    type: :Woman
  AssignClass (201b382a-25e0-48a3-b31a-8535d8fb8c9f)
 Call ID: 201b382a-25e0-48a3-b31a-8535d8fb8c9f
  Args:
    source: :MicaelaAnnaMariaCousinoYQuinonesDeLeon
    type: :Person
  AddLiteral (ae4f0266-c604-44e3-877b-f0ec27322016)
 Call ID: ae4f0266-c604-44e3-877b-f0ec27322016
  Args:
    literal_type: xsd:integer
    literal_value: 1938
    relation: :hasBirthYear
    source: :MicaelaAnnaMariaCousinoYQuinonesDeLeon
  AddLiteral (ffed79b9-52e9-4fe6-836c-7a359118a936)
 Call ID: ffed79b9-52e9-4fe6-836c-7a359118a936
  Args:
    literal_type: xsd:integer
    source: :MicaelaAnnaMariaCousinoYQuinonesDeLeon
    relation: :hasDeathYear
    literal_value: 2022
  AddTriple (d06ee775-1551-47c0-a9dc-e2cf319af609)
 Call ID: d06ee775-1551-47c0-a9dc-e2cf319af609
  Args:
    target: :MicaelaAnnaMariaCousinoYQuinonesDeLeon
    relation: :hasRelation
    source: :HenriPhilippePierreMariedOrleans
  AddLiteral (8dcc64df-4489-485f-84a6-67579f0a9687)
 Call ID: 8dcc64df-4489-485f-84a6-67579f0a9687
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :MicaelaAnnaMariaCousinoYQuinonesDeLeon
    literal_value: 1984
  AssignClass (06d78257-50b5-4261-95c9-ebc5e226ba62)
 Call ID: 06d78257-50b5-4261-95c9-ebc5e226ba62
  Args:
    source: :MarieDaughterOfHenri
    type: :Woman
  AssignClass (de9ec165-8d44-4539-a10a-c8a34b8a7108)
 Call ID: de9ec165-8d44-4539-a10a-c8a34b8a7108
  Args:
    source: :MarieDaughterOfHenri
    type: :Person
  AddTriple (eae3aa69-e2ae-4d83-859f-758c87c9a2ac)
 Call ID: eae3aa69-e2ae-4d83-859f-758c87c9a2ac
  Args:
    target: :HenriPhilippePierreMariedOrleans
    source: :MarieDaughterOfHenri
    relation: :hasFather
  AddTriple (ec70bdcc-ee22-4211-90f1-c8fd84e0c1a1)
 Call ID: ec70bdcc-ee22-4211-90f1-c8fd84e0c1a1
  Args:
    source: :MarieDaughterOfHenri
    relation: :hasMother
    target: :MarieThereseOfWurttemberg
  AssignClass (d5d56e93-3028-4640-9e04-f80daa99c9ab)
 Call ID: d5d56e93-3028-4640-9e04-f80daa99c9ab
  Args:
    type: :Man
    source: :PrinceGundakarOfLiechtenstein
  AssignClass (5dd87436-991c-4a41-bb2f-16b6f7c06db3)
 Call ID: 5dd87436-991c-4a41-bb2f-16b6f7c06db3
  Args:
    type: :Person
    source: :PrinceGundakarOfLiechtenstein
  AddTriple (4561067f-d0bb-4e28-bdb3-ee02c86eb57e)
 Call ID: 4561067f-d0bb-4e28-bdb3-ee02c86eb57e
  Args:
    source: :MarieDaughterOfHenri
    relation: :hasRelation
    target: :PrinceGundakarOfLiechtenstein
  AssignClass (aa1392cb-2ea4-4ef2-8879-b5559cd9abed)
 Call ID: aa1392cb-2ea4-4ef2-8879-b5559cd9abed
  Args:
    source: :LuisCousinoYSebire
    type: :Man
  AssignClass (4287e19e-a207-4dac-b87c-623bd6c11d10)
 Call ID: 4287e19e-a207-4dac-b87c-623bd6c11d10
  Args:
    type: :Person
    source: :LuisCousinoYSebire
  AssignClass (1f9358ed-1248-41b6-a8e6-f43a51597a9d)
 Call ID: 1f9358ed-1248-41b6-a8e6-f43a51597a9d
  Args:
    type: :Woman
    source: :AntoniaMariaQuinonesDeLeonYBanuelos
  AssignClass (53fcc348-faf8-4110-900a-8d381edadb6c)
 Call ID: 53fcc348-faf8-4110-900a-8d381edadb6c
  Args:
    source: :AntoniaMariaQuinonesDeLeonYBanuelos
    type: :Person
  AddTriple (0cdd926a-ff98-4698-b19e-f253a7dc7a1c)
 Call ID: 0cdd926a-ff98-4698-b19e-f253a7dc7a1c
  Args:
    source: :MicaelaAnnaMariaCousinoYQuinonesDeLeon
    relation: :hasFather
    target: :LuisCousinoYSebire
  AddTriple (a4ae8fcf-d814-4580-8b7c-209847e242c9)
 Call ID: a4ae8fcf-d814-4580-8b7c-209847e242c9
  Args:
    source: :MicaelaAnnaMariaCousinoYQuinonesDeLeon
    relation: :hasMother
    target: :AntoniaMariaQuinonesDeLeonYBanuelos
  AssignClass (e4a46159-49c6-4be4-bca6-7fea1e2b4684)
 Call ID: e4a46159-49c6-4be4-bca6-7fea1e2b4684
  Args:
    source: :JeanRobertBoeuf
    type: :Man
  AssignClass (98012a8e-1205-4145-8577-12cf05764d90)
 Call ID: 98012a8e-1205-4145-8577-12cf05764d90
  Args:
    type: :Person
    source: :JeanRobertBoeuf
  AddTriple (2c45a250-1545-4a09-85a6-11deefb7e316)
 Call ID: 2c45a250-1545-4a09-85a6-11deefb7e316
  Args:
    target: :JeanRobertBoeuf
    relation: :hasRelation
    source: :MicaelaAnnaMariaCousinoYQuinonesDeLeon
  AssignClass (1571dcbe-f4bd-4a12-8d62-3f48c35a89d6)
 Call ID: 1571dcbe-f4bd-4a12-8d62-3f48c35a89d6
  Args:
    source: :PrinceJacquesDukeOfOrleans
    type: :Man
  AssignClass (a5fbdfeb-4f11-473e-be69-bf6356b60e8f)
 Call ID: a5fbdfeb-4f11-473e-be69-bf6356b60e8f
  Args:
    source: :PrinceJacquesDukeOfOrleans
    type: :Person
  AddTriple (c08843f8-8884-422f-88dc-3e2d6f344c4c)
 Call ID: c08843f8-8884-422f-88dc-3e2d6f344c4c
  Args:
    source: :PrinceJacquesDukeOfOrleans
    relation: :isBrotherOf
    target: :HenriPhilippePierreMariedOrleans
  AssignClass (087ab564-7fb1-49a9-9357-5534cc9611db)
 Call ID: 087ab564-7fb1-49a9-9357-5534cc9611db
  Args:
    source: :PrinceCharlesLouisDOrleans
    type: :Man
  AssignClass (e9745019-7a52-4c60-bede-88a3aef62ee2)
 Call ID: e9745019-7a52-4c60-bede-88a3aef62ee2
  Args:
    source: :PrinceCharlesLouisDOrleans
    type: :Person
  AddLiteral (0512b03c-b9d9-4427-950a-a7045f3ce087)
 Call ID: 0512b03c-b9d9-4427-950a-a7045f3ce087
  Args:
    literal_type: xsd:integer
    literal_value: 1972
    relation: :hasBirthYear
    source: :PrinceCharlesLouisDOrleans
  AddTriple (3fec637f-4c66-4f65-b234-a34cc6f224d6)
 Call ID: 3fec637f-4c66-4f65-b234-a34cc6f224d6
  Args:
    target: :PrinceJacquesDukeOfOrleans
    source: :PrinceCharlesLouisDOrleans
    relation: :hasFather
  AssignClass (6566dc21-12f7-46c8-9330-b05c90d887bb)
 Call ID: 6566dc21-12f7-46c8-9330-b05c90d887bb
  Args:
    source: :PrinceFoulquesDOrleans
    type: :Man
  AssignClass (93c03c7d-5327-4541-887d-6e3c648a3bf0)
 Call ID: 93c03c7d-5327-4541-887d-6e3c648a3bf0
  Args:
    type: :Person
    source: :PrinceFoulquesDOrleans
  AddLiteral (ef0d9c89-a069-47c0-8176-daa12a53687a)
 Call ID: ef0d9c89-a069-47c0-8176-daa12a53687a
  Args:
    source: :PrinceFoulquesDOrleans
    relation: :hasBirthYear
    literal_value: 1974
    literal_type: xsd:integer
  AddTriple (3387a711-341d-4a58-a84f-45936de333e0)
 Call ID: 3387a711-341d-4a58-a84f-45936de333e0
  Args:
    source: :PrinceFoulquesDOrleans
    relation: :hasFather
    target: :PrinceJacquesDukeOfOrleans
  AssignClass (5b2b23c0-4fd3-4816-8bf9-27c02f30cc11)
 Call ID: 5b2b23c0-4fd3-4816-8bf9-27c02f30cc11
  Args:
    type: :Man
    source: :FrancoisCountOfClermontSonOfHenri
  AssignClass (142f0fbb-40d8-4806-8442-66bcc5981e45)
 Call ID: 142f0fbb-40d8-4806-8442-66bcc5981e45
  Args:
    source: :FrancoisCountOfClermontSonOfHenri
    type: :Person
  AddTriple (4a2939a5-7d5f-4092-9a65-6ec2ab1a3372)
 Call ID: 4a2939a5-7d5f-4092-9a65-6ec2ab1a3372
  Args:
    target: :HenriPhilippePierreMariedOrleans
    source: :FrancoisCountOfClermontSonOfHenri
    relation: :hasFather
  AddTriple (477e2236-6acf-4950-8c2e-96d6cdd7660f)
 Call ID: 477e2236-6acf-4950-8c2e-96d6cdd7660f
  Args:
    relation: :hasMother
    source: :FrancoisCountOfClermontSonOfHenri
    target: :MarieThereseOfWurttemberg
  AssignClass (f1015e3b-0b54-47e1-a51d-86a51b9903ea)
 Call ID: f1015e3b-0b54-47e1-a51d-86a51b9903ea
  Args:
    type: :Man
    source: :PrinceJeanDukeOfVendome
  AssignClass (fbf8c639-c0ca-465f-b0f8-db4c14c868d0)
 Call ID: fbf8c639-c0ca-465f-b0f8-db4c14c868d0
  Args:
    source: :PrinceJeanDukeOfVendome
    type: :Person
  AddTriple (88ecc64f-a94f-49e4-9917-b504229e678c)
 Call ID: 88ecc64f-a94f-49e4-9917-b504229e678c
  Args:
    target: :HenriPhilippePierreMariedOrleans
    source: :PrinceJeanDukeOfVendome
    relation: :hasFather
  AddTriple (dd2d183c-99af-4150-af50-dca378c3de6f)
 Call ID: dd2d183c-99af-4150-af50-dca378c3de6f
  Args:
    source: :PrinceJeanDukeOfVendome
    relation: :hasMother
    target: :MarieThereseOfWurttemberg
  AssignClass (39ae14cf-66b3-4866-a1ed-16032d106b87)
 Call ID: 39ae14cf-66b3-4866-a1ed-16032d106b87
  Args:
    source: :MichelCountOfEvreux
    type: :Man
  AssignClass (083c07cd-6a7c-496f-9945-1d61664f572e)
 Call ID: 083c07cd-6a7c-496f-9945-1d61664f572e
  Args:
    type: :Person
    source: :MichelCountOfEvreux
  AddTriple (0a256827-eb83-4df7-816a-bf5acbb757bf)
 Call ID: 0a256827-eb83-4df7-816a-bf5acbb757bf
  Args:
    source: :MichelCountOfEvreux
    relation: :isBrotherOf
    target: :HenriPhilippePierreMariedOrleans
  AssignClass (47b6efb3-0466-4bf0-a74b-42c173eaa66b)
 Call ID: 47b6efb3-0466-4bf0-a74b-42c173eaa66b
  Args:
    type: :Man
    source: :ThibautCountOfLaMarche
  AssignClass (ec474cf3-2339-4742-ad0d-096a893e9b8c)
 Call ID: ec474cf3-2339-4742-ad0d-096a893e9b8c
  Args:
    source: :ThibautCountOfLaMarche
    type: :Person
  AddTriple (0458c1d7-17cc-49f1-9b1b-cdbaedf465a0)
 Call ID: 0458c1d7-17cc-49f1-9b1b-cdbaedf465a0
  Args:
    target: :HenriPhilippePierreMariedOrleans
    relation: :isBrotherOf
    source: :ThibautCountOfLaMarche
  AssignClass (449a1062-3859-4731-91dd-45543a87837e)
 Call ID: 449a1062-3859-4731-91dd-45543a87837e
  Args:
    type: :Woman
    source: :DianeSisterOfHenri
  AssignClass (ee8adf5b-e383-4deb-9854-b976a2a45030)
 Call ID: ee8adf5b-e383-4deb-9854-b976a2a45030
  Args:
    type: :Person
    source: :DianeSisterOfHenri
  AddTriple (1fea0d90-56eb-4014-ae93-2ded8d431999)
 Call ID: 1fea0d90-56eb-4014-ae93-2ded8d431999
  Args:
    target: :HenriPhilippePierreMariedOrleans
    relation: :isSisterOf
    source: :DianeSisterOfHenri
  Finish (291a5bd4-0bd2-494f-8b99-23825696c88c)
 Call ID: 291a5bd4-0bd2-494f-8b99-23825696c88c
  Args: